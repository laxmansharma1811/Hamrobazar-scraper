from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

driver = webdriver.Chrome()
driver.get("https://hamrobazar.com/")
time.sleep(10)


search_box = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div/div[1]/form/div[1]/input")
search_box.send_keys("iphone")
search_box.send_keys(Keys.RETURN)

time.sleep(10)

def scroll_down(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)

product_links = set()
scroll_attempts = 10
for _ in range(scroll_attempts):
    scroll_down(driver)
    main_img_elements = driver.find_elements(By.CLASS_NAME, 'main-img')
    for element in main_img_elements:
        link = element.find_element(By.TAG_NAME, 'a').get_attribute('href')
        product_links.add(link)

print("Collected product links:", product_links)

time.sleep(5)

seller_infos = []
titles = []
descriptions = []

for link in product_links:
    driver.get(link)
    time.sleep(5)

    try:
        seller_info = driver.find_element(By.CLASS_NAME, "seller__desc").text
        print("Seller Info:", seller_info)
    except Exception as e:
        seller_info = "N/A"
        print("Error extracting seller info:", e)

    try:
        title = driver.find_element(By.CSS_SELECTOR, ".title--relative h3").text
        print("Title:", title)
    except Exception as e:
        title = "N/A"
        print("Error extracting title:", e)

    try:
        description_element = driver.find_element(By.CLASS_NAME, "ad--desc")
       
        show_more_elements = description_element.find_elements(By.CLASS_NAME, "more")
        if show_more_elements:
            for show_more_element in show_more_elements:
                if show_more_element.is_displayed():
                    driver.execute_script("arguments[0].click();", show_more_element)
                    time.sleep(2) 
        description = description_element.text
        print("Description:", description)
    except Exception as e:
        description = "N/A"
        print("Error extracting description:", e)

    seller_infos.append(seller_info)
    titles.append(title)
    descriptions.append(description)

    print("**********************************************************************************")

driver.quit()


data = {
    'Seller Info': seller_infos,
    'Title': titles,
    'Description': descriptions
}
df = pd.DataFrame(data)


csv_filename = 'hamrobazar_iphones.csv'
df.to_csv(csv_filename, index=False, encoding='utf-8')

print(f"Data extracted and saved to {csv_filename}")
