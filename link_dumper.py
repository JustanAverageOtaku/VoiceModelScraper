from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


def initialize() -> webdriver.Chrome:
    options = Options()
    options.add_argument('--headless=old')
    driver = webdriver.Chrome(options=options)
    driver.get("https://voice-models.com")
    return driver


def dump_links(end: int):
    links = []
    count = 1
    driver = initialize()
    wait = WebDriverWait(driver=driver, timeout=10, poll_frequency=1)

    while count <= end:
        print(count)
        try:
            table = driver.find_element(By.CLASS_NAME, "table")
            rows = table.find_elements(By.CLASS_NAME, "fs-5")

            for row in rows:
                ref = row.get_attribute("href")
                if ref is not None:
                    links.append(ref)

            nex = driver.find_element(By.XPATH, "//*[@id=\"pagination\"]/ul")
            nex.find_elements(By.TAG_NAME, "li")[-2].click()

            wait.until(expected_conditions.staleness_of(rows[0]))
        except Exception as e:
            dump("dump.txt", "a", "\n".join(links))
            links.clear()
            if count >= end:
                break
            continue
        count += 1

    dump("dump.txt", "a", "\n".join(links))

    driver.close()


def dump(name: str, mode: str, content: str):
    with open(file=name, mode=mode) as output:
        output.write(content)


if __name__ == "__main__":
    dump_links(898)
    print("Goodbye, World!")
