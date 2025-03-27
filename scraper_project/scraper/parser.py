import re
from bs4 import BeautifulSoup
from scraper_project.scraper.config import settings

def parse_product_list(html_content):
    soup = BeautifulSoup(html_content, "html.parser", from_encoding="utf-8")
    return soup.find_all("div", attrs={"class": settings.PRODUCT_WRAPPER_CLASS})

def extract_product_info(product):
    product_name = product.find("div", attrs={"class": settings.PRODUCT_DESC_CLASS})
    product_name_1 = product.find("span", attrs={"class": settings.PRODUCT_NAME_CLASS})
    product_name_clear = product_name.text.strip() if product_name else None
    product_name_1_clear = product_name_1.text.strip() if product_name_1 else None
    
    original_price = None
    price_selectors = [
        ("div", {"class": settings.PRICE_DISCOUNTED_CLASS}),
        ("div", {"class": settings.PRICE_SELLING_CLASS}),
        ("div", {"class": "prc-box-dscntd"}),
        ("div", {"class": "prc-box-sllng"}),
        ("div", {"class": "product-price"}),
        ("div", {"class": "pr-bx-w"}),
        ("span", {"class": "prc-slg"}),
        ("span", {"class": "prc-dsc"})
    ]
    
    for tag, attrs in price_selectors:
        price_element = product.find(tag, attrs=attrs)
        if price_element:
            original_price = price_element.text.strip()
            break
    
    product_links = product.find_all("div", attrs={"class": settings.PRODUCT_CARD_BORDER_CLASS})
    
    return (product_name_clear, product_name_1_clear, original_price, product_links)

def extract_product_link(link_element):
    link_continue = link_element.find("a")
    if link_continue:
        link_continue = link_continue.get("href")
        return f"https://www.trendyol.com{link_continue}"
    return None

def parse_product_details(detail_html):
    product_details_dict = {}
    detail_soup = BeautifulSoup(detail_html, "html.parser")
    
    price_selectors = [
        ("span", {"class": "prc-dsc"}),
        ("span", {"class": "prc-slg"}),
        ("div", {"class": "product-price-container"}),
        ("div", {"class": "pr-bx-w"}),
        ("div", {"class": "pr-bx-nm with-discount"})
    ]
    
    for tag, attrs in price_selectors:
        price_element = detail_soup.find(tag, attrs=attrs)
        if price_element:
            product_details_dict["Price"] = price_element.text.strip()
            break
    
    parse_main_specifications(detail_soup, product_details_dict)
    
    parse_specification_tables(detail_soup, product_details_dict)
    
    parse_features(detail_soup, product_details_dict)
    
    parse_description(detail_soup, product_details_dict)
    
    return product_details_dict

def parse_main_specifications(soup, details_dict):
    product_specifications = soup.find_all("ul", class_=settings.SPECIFICATIONS_CONTAINER_CLASS)
    for specific in product_specifications:
        details = specific.find_all("li", class_=settings.SPECIFICATION_ITEM_CLASS)
        for i in details:
            label_element = i.find("span")
            value_element = i.find("b")
            
            if label_element and value_element:
                label = label_element.text.strip()
                value = value_element.text.strip()
                details_dict[label] = value

def parse_specification_tables(soup, details_dict):
    spec_tables = soup.find_all("table", class_=settings.PRODUCT_FEATURES_CLASS)
    for table in spec_tables:
        rows = table.find_all("tr")
        for row in rows:
            cells = row.find_all("td")
            if len(cells) >= 2:
                label = cells[0].text.strip()
                value = cells[1].text.strip()
                details_dict[label] = value

def parse_features(soup, details_dict):
    feature_divs = soup.find_all("div", class_=settings.FEATURE_CLASS)
    for div in feature_divs:
        label_elem = div.find("span", class_=settings.FEATURE_NAME_CLASS)
        value_elem = div.find("span", class_=settings.FEATURE_VALUE_CLASS)
        if label_elem and value_elem:
            label = label_elem.text.strip()
            value = value_elem.text.strip()
            details_dict[label] = value

def parse_description(soup, details_dict):
    description = soup.find("div", class_=settings.PRODUCT_DESCRIPTION_CLASS)
    if description:
        desc_text = description.text
        common_specs = [
            ("RAM", r"RAM:\s*(\d+\s*GB)"),
            ("Storage", r"Storage:\s*(\d+\s*GB)"),
            ("Camera", r"Camera:\s*(\d+\s*MP)"),
            ("Battery", r"Battery:\s*(\d+\s*mAh)")
        ]
        
        for spec_name, pattern in common_specs:
            match = re.search(pattern, desc_text)
            if match and spec_name not in details_dict:
                details_dict[spec_name] = match.group(1) 