import scraping_tenkijp


if __name__ == "__main__":
    Otenki = scraping_tenkijp.Otenki()
    print(Otenki.get_weather())