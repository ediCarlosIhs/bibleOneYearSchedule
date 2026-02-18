from pyscript import web, when
import js
import json
from bible import bible_first_column, bible_second_column, bible_third_column
from datetime import date

def save_initial_data():

    # verify is data exists in Local Storage
    existing_bible = js.localStorage.getItem("bible")
    existing_progress = js.localStorage.getItem("progress")
    existing_dates = js.localStorage.getItem("dates")

    if not existing_bible:
        # Data to save
        date_to_save = {
            "bible_first_column": bible_first_column,
            "bible_second_column": bible_second_column,
            "bible_third_column": bible_third_column
        }

        # convert to JSON (string)
        json_data = json.dumps(date_to_save)

        # Save to local storage in the browser
        js.localStorage.setItem("bible", json_data)
        # print("bible saved in local storage!")

    if not existing_progress:

        progress = []

        progress_data = json.dumps(progress)

        js.localStorage.setItem("progress", progress_data)

        print("progress saved in Local Storage!")

    if not existing_dates:

        dates = {}

        saved_dates = json.dumps(dates)

        js.localStorage.setItem("dates", saved_dates)

def load_bible():
    stored_bible = js.localStorage.getItem("bible")

    if stored_bible:
        return json.loads(stored_bible)
    
def load_progress():
    stored_progress = js.localStorage.getItem("progress")

    if stored_progress:
        return json.loads(stored_progress)
    
def load_dates():
    stored_dates = js.localStorage.getItem("dates")

    if stored_dates:
        return json.loads(stored_dates)

def save_bible_progress(bible_column: str, book: str, chapter: str, is_checked: bool):
    stored_bible = js.localStorage.getItem("bible")

    if stored_bible:
        bible = json.loads(stored_bible)

        bible[bible_column][book][chapter] = is_checked
    
    js.localStorage.setItem("bible", json.dumps(bible))

def save_date_history(classification_date, date):
    stored_dates = js.localStorage.getItem("dates")

    if stored_dates:
        dates = json.loads(stored_dates)

        dates[classification_date] = date
    
    js.localStorage.setItem("dates", json.dumps(dates))

def save_day_progress(day: str, is_checked: bool):
    stored_progress = js.localStorage.getItem("progress")

    progress = json.loads(stored_progress) if stored_progress else []

    if day not in progress:

        progress.append(day)
    
    elif not is_checked:

        if day in progress:
            day_index = progress.index(day)
            del progress[day_index]

    js.localStorage.setItem("progress", json.dumps(progress))

def create_sections(id):
    # select the main element
    main_elements = web.page.find("main")

    if not main_elements:
        return

    main = main_elements[0]

    # create an empty section
    section = web.section(classes=["block"], id=f"block-{id}")

    # Block for dates

    # create div for date
    date_div = web.div(class_="date")

    # fieldset for begin date
    saved_date = load_dates()
    fs_start = web.fieldset()
    if not saved_date or "begin_date" not in saved_date:
        today = date.today().strftime("%Y-%m-%d")
        saved_date = {"begin_date": today}

    fs_start.append(web.label("Begin Date:", for_="dateStarted"))
    fs_start.append(web.input_(type="date", name="dateStarted", id="dateStarted", value=saved_date["begin_date"], onchange=handle_date_change))

    # fieldset Actual block begin date
    saved_date = load_dates()
    if not saved_date or "block_begin" not in saved_date:
        today = date.today().strftime("%Y-%m-%d")
        saved_date = {"block_begin": today}
    fs_block = web.fieldset()
    fs_block.append(web.label("This Block Begin Date:", for_="dateOfThisBlock"))
    fs_block.append(web.input_(type="date", name="dateOfThisBlock", id="dateOfThisBlock", value=saved_date["block_begin"], onchange=handle_date_change))

    date_div.append(fs_start)
    date_div.append(fs_block)
    section.append(date_div)

    # Block for the controller
    controller_div = web.div(class_="controller")

    # Show sections div
    show_div = web.div(class_="show__sections")
    show_div.append(web.label("Show Sections", for_=f"show_section-{id}"))
    show_div.append(web.input_(type="checkbox", name=f"show_section-{id}", id=f"show_section-{id}"))

    # Activate Section
    activate_div = web.div(class_="activate")
    activate_div.append(web.label("Activate Section", for_=f"activate-{id}"))
    activate_div.append(web.input_(type="checkbox", name=f"activate-{id}", id=f"activate-{id}"))

    controller_div.append(show_div)
    controller_div.append(activate_div)
    section.append(controller_div)

    # Block for the header
    header_div = web.div(class_="header")
    day_p = web.p("Day")
    scripture_p = web.p("Scripture")
    new_testament_p = web.p("New Testament")

    header_div.append(day_p)
    header_div.append(scripture_p)
    header_div.append(new_testament_p)

    section.append(header_div)

    main.append(section)

def get_key(dict):
    return list(dict.keys())[0]

def handle_date_change(event):
    new_date = event.target.value

    event_id = event.target.id

    print(event_id)

    if event_id == "dateStarted":
        save_date_history("begin_date", new_date)
    elif event_id == "dateOfThisBlock":
        save_date_history("block_begin", new_date)

def handle_check_click(event):

    checkbox = event.target

    parent_div = checkbox.parentElement
    label = checkbox.nextElementSibling

    checkbox_id = checkbox.id
    is_checked = checkbox.checked

    if "days" in parent_div.classList:
        day = label.innerText
        save_day_progress(day, is_checked)
    else:
        bible_column = parent_div.className
        book = getattr(checkbox, "data_book", "")
        chapter = getattr(checkbox, "data_chapter", "")
        save_bible_progress(bible_column, book, chapter, is_checked)

        # print(f"Checkbox {checkbox_id} clicked for: {is_checked}")
        # print(f"book: {book}, chapter: {chapter}" )

def insert_row(id, line_number, day_status, first_book: str, first_book_chapter, status_first_book_chapter, second_book: str, second_book_chapter, status_second_book_chapter, third_book: str, third_book_chapter, status_third_book_chapter):
    # print(first_book_chapter)
    section = web.page[f"block-{id}"]

    # Block for the row div
    row_div = web.div(class_="row")

    # days
    days_div = web.div(class_="days")
    days_div.append(web.input_(type="checkbox", name=f"checkpoint-{line_number}", id=f"checkpoint-{line_number}", on_click=handle_check_click, checked=day_status))
    days_div.append(web.label(line_number, for_=f"checkpoint-{line_number}"))

    # first_column div
    first_column_div = web.div(class_="bible_first_column")
    first_column_div.append(web.input_(type="checkbox", name=f"{first_book}-{first_book_chapter}", id=f"{first_book}-{first_book_chapter}", on_click=handle_check_click, data_book=f"{first_book}", data_chapter=f"{first_book_chapter}", checked=status_first_book_chapter))
    first_column_div.append(web.label(f"{first_book.capitalize()} {first_book_chapter}", for_=f"{first_book}-{first_book_chapter}"))

    # second_column div
    second_column_div = web.div(class_="bible_second_column")
    second_column_div.append(web.input_(type="checkbox", name=f"{second_book}-{second_book_chapter}", id=f"{second_book}-{second_book_chapter}", on_click=handle_check_click, data_book=f"{second_book}", data_chapter=f"{second_book_chapter}", checked=status_second_book_chapter))
    second_column_div.append(web.label(f"{second_book.capitalize()} {second_book_chapter}", for_=f"{second_book}-{second_book_chapter}"))

    # third_column div
    third_column_div = web.div(class_="bible_third_column")
    third_column_div.append(web.input_(type="checkbox", name=f"{third_book}-{third_book_chapter}", id=f"{third_book}-{third_book_chapter}", on_click=handle_check_click, data_book=f"{third_book}", data_chapter=f"{third_book_chapter}", checked=status_third_book_chapter))
    third_column_div.append(web.label(f"{third_book.capitalize()} {third_book_chapter}", for_=f"{third_book}-{third_book_chapter}"))

    row_div.append(days_div)
    row_div.append(first_column_div)
    row_div.append(second_column_div)
    row_div.append(third_column_div)

    section.append(row_div)

def get_column_dict(column, book, begin_chapter, end_chapter):
    """
    Get the book, begin chapter, and end_chapter
    return a dict with the book name and the chapters.

    parameters
    book: the desired book to create a dict
    begin_chapter: the begin chapter of the dict to be returned
    end_chapter: the last chapter of the book to be returned in the dictionary
    """
    # js.eval("debugger;")
    book_dict = {}
    list_of_chapters = []

    if book in column:
        
        actual_book = column.get(book)

        for key in actual_book:
            if begin_chapter in actual_book and end_chapter in actual_book:
                list_of_chapters.append({key: actual_book[key]})
            
            if key == end_chapter:
                break

    book_dict[book] = list_of_chapters

    return book_dict

def draw_first_section(bible):
    first_column = get_column_dict(bible["bible_first_column"], "gen", "1", "46-47")
    second_column = get_column_dict(bible["bible_second_column"], "ps", "1", "29")
    third_column = get_column_dict(bible["bible_third_column"], "mt", "1.1-17", "16")

    progress = load_progress()

    lines = len(first_column["gen"])

    for line in range(lines):

        day_status = False
        if str(line + 1) in progress:
            day_status = True
        
        key_first_book_column = get_key(first_column["gen"][line])
        status_first_book_column = first_column["gen"][line][key_first_book_column]

        key_second_book_column = get_key(second_column["ps"][line])
        status_second_book_column = second_column["ps"][line][key_second_book_column]

        key_third_book_column = get_key(third_column["mt"][line])
        status_third_book_column = third_column["mt"][line][key_third_book_column]

        insert_row(1, line + 1, day_status, "gen", key_first_book_column, status_first_book_column, "ps", get_key(second_column["ps"][line]), status_second_book_column, "mt", get_key(third_column["mt"][line]), status_third_book_column)

def lock_first_section():
    first_section_checkbox = web.page["activate-1"]
    first_section_checkbox.checked = True
    first_section_checkbox.disabled = True

def main():

    bible = load_bible()
    save_initial_data()

    create_sections(1)

    draw_first_section(bible)
    lock_first_section()

main()




