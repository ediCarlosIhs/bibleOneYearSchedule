def get_key(dict):
    return list(dict.keys())[0]

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