import json

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from link_dumper import dump


def initialize() -> webdriver.Chrome:
    options = Options()
    options.add_argument('--headless=old')
    driver = webdriver.Chrome(options=options)
    return driver


def load(name: str) -> list[str]:
    with open(file=name, mode="r") as inputs:
        return list(inputs)


def orchestrator(start: int, end: int):
    driver = initialize()

    links = load("dump.txt")
    for i in range(start, end):
        print(i)
        driver.get(links[i])

        name = driver.find_element(By.XPATH, "//*[@id=\"kt_app_content_container\"]/div/div/div/div[1]/div/h3")
        created_at = driver.find_element(By.XPATH, "//*[@id=\"kt_app_content_container\"]/div/div/div/div[1]/div/small")
        image = driver.find_element(By.XPATH, "//*[@id=\"kt_app_content_container\"]/div/div/div/div[2]/div[1]/img").get_attribute("src")
        details = driver.find_element(By.XPATH, "//*[@id=\"kt_app_content_container\"]/div/div/div/div[2]/div[2]/p[1]")
        tags = driver.find_element(By.XPATH, "//*[@id=\"kt_app_content_container\"]/div/div/div/div[2]/div[2]/p[2]")
        download = driver.find_element(By.XPATH, "//*[@id=\"kt_app_content_container\"]/div/div/div/div[2]/div[2]/p[3]/a[1]").get_attribute("href")

        dump(
            "models.jsonl",
            "a",
            json.dumps(
                {
                    "name": name.text,
                    "ref": links[i],
                    "created_at": created_at.text,
                    "image": image,
                    "details": details.text,
                    "tags": tags.text,
                    "download": download
                }
            ) + "\n"
        )

    driver.close()


if __name__ == "__main__":
    orchestrator(22450, 22451)
    print("Goodbye, World!")
