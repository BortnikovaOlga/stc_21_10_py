from app import Application


# def test_1():
#     main_page = MainPage()
#     main_page.open_main_page()
#     assert "Python" in main_page.get_title()
#     main_page.search("pycon")
#     assert "No results found." not in main_page.get_page_source()
#     main_page.quit()


def test_2():
    app = Application()
    app.main_page.open_main_page()
    app.main_page.search("pycon")
    assert "No results found." not in app.main_page.page_source()
    app.quit()

test_2()
