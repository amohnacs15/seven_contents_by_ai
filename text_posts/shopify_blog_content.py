# Shopify Blog Upload
import shopify
import appsecrets


def initialize_shopify():
    # Configure store details
    shop_url = 'osaka-cosplay.myshopify.com'
    admin_api_key = appsecrets.SHOPIFY_ADMIN_API_TOKEN
    api_version = '2023-01'
    # Create and activate a new session
    session = shopify.Session(shop_url, api_version, admin_api_key)
    shopify.ShopifyResource.activate_session(session)

def upload_shopify_blog_article(filePath, blog):
    blogfile = open(filePath, 'r')
    bloglines = blogfile.readlines()

    title = bloglines[0].replace("# H1: ", " ").strip()
    title = bloglines[0].replace("#H1 - ", " ").strip()
    title = bloglines[0].replace("#H1 ", " ").strip()
    title = bloglines[0].replace("#", " ").strip()
    
    new_blog = shopify.Blog.create({"title": title})
    if (new_blog.save()):
        new_article = shopify.Article()

        new_article.title = title
        new_article.author = "Caregiver Modern"
        new_article.blog_id = new_blog.id
        new_article.body_html = blog
        # new_article.image = createMidjourneyImage("default", 1024, 768)
        new_article.published = 'TRUE'
        new_article.save()
        print ("Shopify article upload successful")
    else:
        print (blog.errors.full_messages())