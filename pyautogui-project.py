import os
import asyncio
import httpx
import aiofiles
import pyautogui
import sys
from pyscreeze import ImageNotFoundException
from typing import Optional, List
from aioconsole import ainput


async def create_directory(directory_name: str) -> None:
    directory_path = os.path.join(os.path.expanduser("~"), "Desktop", directory_name)

    def create_directory_if_not_exists() -> None:
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
            print(f"Directory '{directory_name}' created on Desktop.")
        else:
            print(f"Directory '{directory_name}' already exists on Desktop.")

    try:
        await asyncio.get_running_loop().run_in_executor(
            None, create_directory_if_not_exists
        )
    except PermissionError as e:
        print(f"Permission error creating directory '{directory_name}': {e}")
    except OSError as e:
        print(f"OS error creating directory '{directory_name}': {e}")
    except Exception as e:
        print(f"Unexpected error creating directory '{directory_name}': {e}")


async def fetch_json_from_url(url: str) -> Optional[dict]:
    try:
        async with httpx.AsyncClient(verify=False, http2=True) as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as e:
        print(f"Error fetching URL '{url}': {e}")
    except httpx.HTTPStatusError as e:
        print(f"HTTP error fetching URL '{url}': {e}")
    except ValueError as e:
        print(f"Error parsing JSON response from URL '{url}': {e}")
    except Exception as e:
        print(f"Unexpected error fetching URL '{url}': {e}")
    return None


async def open_directory_in_explorer(directory_path: str) -> None:
    try:
        if sys.platform.startswith("win"):
            await asyncio.create_subprocess_shell(f'explorer "{directory_path}"')
        elif sys.platform == "darwin":
            await asyncio.create_subprocess_exec("open", directory_path)
        else:
            await asyncio.create_subprocess_exec("xdg-open", directory_path)
    except FileNotFoundError as e:
        print(f"File not found error opening directory: {e}")
    except PermissionError as e:
        print(f"Permission error opening directory: {e}")
    except Exception as e:
        print(f"Unexpected error opening directory: {e}")


async def create_text_files(
    directory_path: str, file_count: int, file_queue: asyncio.Queue
) -> None:
    try:
        for index in range(file_count):
            file_path = os.path.join(directory_path, f"post_{index}.txt")
            try:
                async with aiofiles.open(file_path, "w") as file:
                    await file.write("")
                print(f"Text file 'post_{index}.txt' created in '{directory_path}'.")
                await file_queue.put(f"post_{index}.txt")
            except PermissionError as e:
                print(f"Permission error creating text file 'post_{index}.txt': {e}")
            except OSError as e:
                print(f"OS error creating text file 'post_{index}.txt': {e}")
            except Exception as e:
                print(f"Unexpected error creating text file 'post_{index}.txt': {e}")
        await file_queue.put(None)
    except Exception as e:
        print(f"Unexpected error creating text files: {e}")


async def add_post_to_queue(post_id: int, post_queue: asyncio.Queue) -> None:
    try:
        json_data = await fetch_json_from_url(
            f"https://jsonplaceholder.typicode.com/posts/{post_id}"
        )
        if json_data:
            await post_queue.put((json_data["title"], json_data["body"]))
        else:
            await post_queue.put((None, None))
    except KeyError as e:
        print(f"Key error adding post data to the queue: {e}")
    except Exception as e:
        print(f"Unexpected error adding post data to the queue: {e}")


async def empty_queue(queue: asyncio.Queue) -> None:
    try:
        while not queue.empty():
            await queue.get()
            queue.task_done()
    except Exception as e:
        print(f"Error emptying queue: {e}")


async def locate_icon_positions(
    expected_count: int, icon_positions_queue: asyncio.Queue
) -> None:
    loop = asyncio.get_running_loop()
    positions: List = []
    try:
        attempts = 0
        max_attempts = 10
        while len(positions) != expected_count and attempts < max_attempts:
            try:
                await empty_queue(icon_positions_queue)
                positions = await loop.run_in_executor(
                    None,
                    lambda: list(
                        pyautogui.locateAllOnScreen("notepad_icon.png", confidence=0.85)
                    ),
                )
                positions = await sort_coordinates_by_y(positions)
                if len(positions) == expected_count:
                    print(f"Found {len(positions)} text file(s).")
                    for pos in set(positions):
                        await icon_positions_queue.put(pos)
                    break
                elif not positions:
                    print("No text file icons found on the screen.")
                attempts += 1
            except ImageNotFoundException:
                print("Image not found while locating icons.")
            except Exception as e:
                print(f"Unexpected error locating icon positions: {e}")

        if len(positions) != expected_count:
            print(
                f"Warning: Expected {expected_count} positions but found {len(positions)}."
            )

    except Exception as e:
        print(f"Unexpected error in locate_icon_positions: {e}")


async def activate_notepad_window(file_name: str) -> bool:
    attempts = 0
    max_attempts = 5
    try:
        while attempts < max_attempts:
            notepad_windows = await asyncio.get_running_loop().run_in_executor(
                None, pyautogui.getWindowsWithTitle, f"{file_name} - Notepad"
            )
            if notepad_windows:
                notepad_window = notepad_windows[0]
                await asyncio.get_running_loop().run_in_executor(
                    None, notepad_window.activate
                )
                return True
            else:
                await asyncio.sleep(0.2)
                attempts += 1
        return False
    except AttributeError as e:
        print(f"Attribute error activating Notepad window: {e}")
    except Exception as e:
        print(f"Unexpected error activating Notepad window: {e}")
        return False


async def sort_coordinates_by_y(
    coordinates: List,
) -> List:
    try:
        return sorted(coordinates, key=lambda coord: coord[1])
    except TypeError as e:
        print(f"Type error sorting coordinates by y-coordinate: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error sorting coordinates by y-coordinate: {e}")
        return []


async def handle_notepad_interaction(
    file_queue: asyncio.Queue, post_queue: asyncio.Queue
) -> None:
    loop = asyncio.get_running_loop()
    try:
        file_name = await file_queue.get()
        if file_queue.empty() or file_name is None:
            print("There is no file")
            file_queue.task_done()
            return
        if not await activate_notepad_window(file_name):
            print(f"Failed to activate Notepad for '{file_name}'")
            return
        await asyncio.sleep(1)
        title, body = await post_queue.get()
        if title is None:
            file_queue.task_done()
            print("There is no title to write.")
            return
        await asyncio.sleep(1)
        pyautogui.write(f"\t{title}\n\n\t{body}", interval=0.1)
        await loop.run_in_executor(None, pyautogui.hotkey, "ctrl", "s")
        await loop.run_in_executor(None, pyautogui.hotkey, "alt", "f4")
    except pyautogui.FailSafeException as e:
        print(f"PyAutoGUI failsafe triggered during Notepad interaction: {e}")
    except Exception as e:
        print(f"Unexpected error handling Notepad interaction: {e}")


async def process_icon_positions(icon_positions_queue: asyncio.Queue) -> None:
    loop = asyncio.get_running_loop()
    try:
        position = await icon_positions_queue.get()
        if position is None:
            return
        center_x, center_y = pyautogui.center(position)
        await loop.run_in_executor(None, pyautogui.moveTo, center_x, center_y)
        await loop.run_in_executor(None, pyautogui.doubleClick)
        icon_positions_queue.task_done()
    except TypeError as e:
        print(f"Type error processing icon positions: {e}")
    except Exception as e:
        print(f"Unexpected error processing icon positions: {e}")


async def main() -> None:

    file_queue = asyncio.Queue()
    file_count = int(await ainput("number of files : "))
    directory_name = await ainput("directory name : ")
    icon_positions_queue = asyncio.Queue()
    post_queue = asyncio.Queue()
    directory_path = os.path.join(os.path.expanduser("~"), "Desktop", directory_name)

    try:
        await create_directory(directory_name)
        await create_text_files(directory_path, file_count, file_queue)
        await open_directory_in_explorer(directory_path)
        await asyncio.sleep(1)
        await locate_icon_positions(file_count, icon_positions_queue)
        for i in range(1, file_count + 1):
            await asyncio.gather(
                process_icon_positions(icon_positions_queue),
                add_post_to_queue(i, post_queue),
            )
            await asyncio.sleep(2)
            await handle_notepad_interaction(file_queue, post_queue)
    except Exception as e:
        print(f"Unexpected error in main function: {e}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Program interrupted by user.")
    except Exception as e:
        print(f"Unexpected error running the program: {e}")
