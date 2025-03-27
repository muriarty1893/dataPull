"""
Parser module for the scraper.
Contains functions for parsing HTML content.
"""
import re
from bs4 import BeautifulSoup
from scraper_project.scraper.config import settings

def parse_product_list(html_content):
    """
    Parse a list of products from HTML content.
    
    Args:
        html_content: HTML content to parse
        
    Returns:
        list: List of BeautifulSoup objects representing products
    """
    soup = BeautifulSoup(html_content, "html.parser", from_encoding="utf-8")
    return soup.find_all("div", attrs={"class": settings.PRODUCT_WRAPPER_CLASS})

def extract_product_info(product):
    """
    Extract basic product information.
    
    Args:
        product: BeautifulSoup object representing a product
        
    Returns:
        tuple: (product_name_clear, product_name_1_clear, original_price, product_links)
    """
    # Extract product name
    product_name = product.find("div", attrs={"class": settings.PRODUCT_DESC_CLASS})
    product_name_1 = product.find("span", attrs={"class": settings.PRODUCT_NAME_CLASS})
    product_name_clear = product_name.text.strip() if product_name else None
    product_name_1_clear = product_name_1.text.strip() if product_name_1 else None
    
    # Extract price
    product_price = product.find("div", attrs={"class": settings.PRICE_DISCOUNTED_CLASS})
    if not product_price:
        product_price = product.find("div", attrs={"class": settings.PRICE_SELLING_CLASS})
    original_price = product_price.text.strip() if product_price else None
    
    # Extract product links
    product_links = product.find_all("div", attrs={"class": settings.PRODUCT_CARD_BORDER_CLASS})
    
    return (product_name_clear, product_name_1_clear, original_price, product_links)

def extract_product_link(link_element):
    """
    Extract product link from a link element.
    
    Args:
        link_element: BeautifulSoup object representing a link
        
    Returns:
        str: Full URL of the product detail page
    """
    link_continue = link_element.find("a")
    if link_continue:
        link_continue = link_continue.get("href")
        return f"https://www.trendyol.com{link_continue}"
    return None

def parse_product_details(detail_html):
    """
    Parse product details from a product detail page.
    
    Args:
        detail_html: HTML content of the product detail page
        
    Returns:
        dict: Dictionary of product details
    """
    product_details_dict = {}
    detail_soup = BeautifulSoup(detail_html, "html.parser")
    
    # Get main specifications
    parse_main_specifications(detail_soup, product_details_dict)
    
    # Get specifications from tables
    parse_specification_tables(detail_soup, product_details_dict)
    
    # Get features
    parse_features(detail_soup, product_details_dict)
    
    # Get specs from description
    parse_description(detail_soup, product_details_dict)
    
    return product_details_dict

def parse_main_specifications(soup, details_dict):
    """
    Parse main product specifications from the detail page.
    
    Args:
        soup: BeautifulSoup object of the detail page
        details_dict: Dictionary to update with specifications
    """
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
    """
    Parse specification tables from the detail page.
    
    Args:
        soup: BeautifulSoup object of the detail page
        details_dict: Dictionary to update with specifications
    """
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
    """
    Parse product features from the detail page.
    
    Args:
        soup: BeautifulSoup object of the detail page
        details_dict: Dictionary to update with specifications
    """
    feature_divs = soup.find_all("div", class_=settings.FEATURE_CLASS)
    for div in feature_divs:
        label_elem = div.find("span", class_=settings.FEATURE_NAME_CLASS)
        value_elem = div.find("span", class_=settings.FEATURE_VALUE_CLASS)
        if label_elem and value_elem:
            label = label_elem.text.strip()
            value = value_elem.text.strip()
            details_dict[label] = value

def parse_description(soup, details_dict):
    """
    Parse product description for specifications.
    
    Args:
        soup: BeautifulSoup object of the detail page
        details_dict: Dictionary to update with specifications
    """
    description = soup.find("div", class_=settings.PRODUCT_DESCRIPTION_CLASS)
    if description:
        desc_text = description.text
        # Look for common phone specs pattern like "RAM: 8GB"
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