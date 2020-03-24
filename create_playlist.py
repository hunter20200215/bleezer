import time
import pickle
import selenium.webdriver 
import csv

from selenium.webdriver.common.keys import Keys

default_timeout = 50

driver = selenium.webdriver.Chrome()
driver.get("https://www.deezer.com")

driver.implicitly_wait(default_timeout)
# load cookie {
try:
    cookies = pickle.load(open("cookies.pkl", "rb"))
except:
    cookies = []

for cookie in cookies:
    # print(cookie)
    if 'expiry' in cookie:
        del cookie['expiry']
    driver.add_cookie(cookie)

#return True if not logged in
def is_loggedin():
    ret = True
    driver.get("https://www.deezer.com/en")
    try:
        driver.implicitly_wait(50)
        driver.find_element_by_id('page_topbar')
        print ("you have login cookie now,so you don't need to login again")
    except:
        ret = False
    driver.implicitly_wait(default_timeout)
    return ret

# } end of cookie load


#test if logged in

if not is_loggedin() :

    
    driver.find_element_by_id('topbar-login-button').click()
    driver.implicitly_wait(5)
    login_email=driver.find_element_by_id('login_mail')
    login_email.send_keys("danny.spaziano1976@icloud.com")
    login_password=driver.find_element_by_id('login_password')
    login_password.send_keys("ThePa55w0rd123?")

    driver.find_element_by_id('login_form_submit').click()
    print ("logging in...")
    driver.implicitly_wait(100)
    driver.find_element_by_id('page_topbar')
    driver.implicitly_wait(default_timeout)
    # save cookie
    pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))

print('now you are logged in')


#=============================   =================
search_box = driver.find_element_by_css_selector('input.topbar-search-input')
with open('playlist.csv', 'r') as csvfile:
    obj = csv.reader(csvfile, skipinitialspace=True)
    next(obj)
    print(obj)
    my_playlist_name="Should Work Final Version"

    # Open sidebar? Doesn't seem to be necessary

    playlists = driver.find_element_by_xpath("//span[text()='Playlists']")
    playlists.click()

    time.sleep(5)

    add_playlist_button = driver.find_element_by_xpath("//button[@aria-label='Create a playlist']")
    driver.execute_script("arguments[0].click();", add_playlist_button)

    time.sleep(2)

    playlist_name_input = driver.find_element_by_xpath("//input[@placeholder='Playlist name']")
    driver.execute_script("arguments[0].click();", playlist_name_input)
    playlist_name_input.send_keys(Keys.CONTROL, "a")
    playlist_name_input.send_keys(my_playlist_name)

    time.sleep(2)
    Add_playlist_createnew_Title=driver.find_element_by_xpath("//button[@id='modal_playlist_assistant_submit']")
    driver.execute_script("arguments[0].click();", Add_playlist_createnew_Title)
    time.sleep(5)

    for row in obj:
        if len(row[0])==0:
            continue
        art_name = row[0]
        abm_name = row[1]
        driver.implicitly_wait(5)
        search_box = driver.find_element_by_css_selector('input.topbar-search-input')
        search_box.send_keys(art_name + ' ' + abm_name)
        search_box.send_keys(Keys.ENTER)
        driver.implicitly_wait(10)
        album_link = driver.find_element_by_xpath(f"//a[@itemprop='inAlbum' and text()='{abm_name}']")
        driver.execute_script("arguments[0].click();", album_link)

        time.sleep(5)

        select_all = driver.find_element_by_xpath("//input[@data-target='checkall']")
        driver.execute_script("arguments[0].click();", select_all)

        time.sleep(5)
        add_to_playlist_button =driver.find_element_by_xpath("//button[@aria-label='Add to playlist']")
        driver.execute_script("arguments[0].click();", add_to_playlist_button)

        time.sleep(5)

        playlist_to_add_to = driver.find_element_by_xpath(f"//span[text()='{my_playlist_name}']/..")
        driver.execute_script("arguments[0].click();", playlist_to_add_to)

        time.sleep(5)

    print("done")
