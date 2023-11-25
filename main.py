from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
import csv

EMPTY_ELEMENT = None                  # Replace with anything u want on empty places in csv file

def get_image_src(blog: WebElement):
    '''Returns the image url of blog'''
    try:
        img = blog.find_element(by=By.CLASS_NAME,value="img")
        img_anchor = img.find_element(by=By.TAG_NAME,value="a")
        img_src = img_anchor.get_attribute("data-bg")
    except:
        img_src = EMPTY_ELEMENT
    return img_src

def get_blog_content(blog: WebElement):
    '''Returns heading,date and likes of blog'''

    try:
        content = blog.find_element(by=By.CLASS_NAME,value="content")
        content_heading = content.find_element(by=By.TAG_NAME,value='h6')
        content_heading_anchor = content_heading.find_element(by=By.TAG_NAME,value="a")
        content_heading_text = content_heading_anchor.text
    except:
        content_heading_text = EMPTY_ELEMENT

    try:
        date_class = content.find_element(by=By.CLASS_NAME,value="bd-item")
        date_span = date_class.find_element(by=By.TAG_NAME,value="span")
        date = date_span.text
    except:
        date = EMPTY_ELEMENT

    try:
        likes_class = content.find_element(by=By.CLASS_NAME,value="zilla-likes")
        likes_span = likes_class.find_element(by=By.TAG_NAME,value="span")
        likes = likes_span.text
    except:
        likes = EMPTY_ELEMENT


    return content_heading_text,date,likes


def click_next(driver):
    '''Return the next page url'''
    try:
        pagination = driver.find_element(by=By.CLASS_NAME,value="pagination")
        next = pagination.find_element(by=By.CLASS_NAME,value="next")
        new_link = next.get_dom_attribute("href")
    except:
        new_link = EMPTY_ELEMENT
    return new_link


def find_blogs(driver):
    ''' Returns array of dict of required data of each blog'''
    blogs_data = []
    blogs = driver.find_elements(by=By.CLASS_NAME,value="blog-item")    # Get the element of blog-item
    print("blogs found",len(blogs))
    for blog in blogs:                                         #Iterate over each blog element 
        img_src = get_image_src(blog)                          # Extract img url
        heading,date,likes = get_blog_content(blog)
        temp = {"img": img_src, "heading": heading, "date": date, "likes": likes}
        blogs_data.append(temp)
    return blogs_data
    




def write_csv(arr,name):
    '''Helper function to write the csv file'''
    keys = arr[0].keys()   # get the header for csv file

    with open(name,'w',newline='') as output_file:
        writer = csv.DictWriter(output_file,keys)     
        writer.writeheader()
        writer.writerows(arr)                       # Write the dict to the file







    
    
def main():
    driver = webdriver.Edge()               # Get the install driver instance, Edge is used if edge not present Chrome can be used
    url = "https://rategain.com/blog"
    driver.get(url)
    blogs =[]
    while True:
        blogs.extend(find_blogs(driver))    # save the blogs to blogs array
        next_link = click_next(driver)      # update next_link with next page link
        print(next_link)
        if next_link==None:
            break
        driver.get(next_link)

    write_csv(blogs,"blogs.csv")



if __name__=="__main__":
    main()




