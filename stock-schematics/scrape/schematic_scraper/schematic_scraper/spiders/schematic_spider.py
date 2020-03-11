import scrapy
import re
import os

# TODO: Get name from category screen!
#       Put name in dictionary with schematic number
#       <a href="/schematic/14123">schematic_name</a>



class SchematicSpider(scrapy.Spider):
    name = "schematics"
    schem_dict = {} # schematic number: schematic name
    category = "etc"

    def start_requests(self):
        urls = [
            "https://www.minecraft-schematics.com/login/",
            # "https://www.minecraft-schematics.com/category/houses-and-shops/",
            # "https://www.minecraft-schematics.com/schematic/14008/download/"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        url = response.url.split("/")
        print("\n\n", url, "\n\n")
        if "login" in url:
            print("Logging in")
            yield scrapy.FormRequest.from_response(
                response,
                formdata={'email':'connorrwilhelm@gmail.com', 'password':'t2dofij0234jo534'},
                callback=self.after_login
            )
            # time.sleep(5) # give it time to login before scraping

        if "category" in url:
            # screen w/ multiple schematics
            self.category = url[4]
            body_str = str(response.body)
            schematic_titles = list(set(re.findall(r'<a href="/schematic/\d+/">[\s\d\w]*</a>', body_str)))
            schematic_set = []
            # TODO: split title into schematic number and letter
            for title in schematic_titles:
                schem_name = re.search(r'>[\s\d\w]*<', title)[0][1:-1]
                schem_num = re.search(r'/\d*/',title)[0][1:-1]
                schematic_set.append(schem_num)
                self.schem_dict[schem_num] = schem_name
            print(self.schem_dict)
            # schematic_set = list(set(re.findall(r"/schematic/\d+/", body_str)))
            print("Found the following schematics: {}".format(schematic_set))
            for schematic in schematic_set:
                yield scrapy.Request(url="https://www.minecraft-schematics.com/schematic/{}/download/action/?type=schematic".format(schematic), callback=self.parse)
                yield scrapy.Request(url="https://www.minecraft-schematics.com/schematic/{}/download/action/?type=schematic".format(schematic), callback=self.parse)

        if "download" in url:
            print("download screen:", url)
            # TODO: get schem_num and then get the name
            schem_num = url[4]
            schem_name = self.schem_dict[schem_num] + ".schematic"
            folder = os.path.join(r"../../scraped_schematics", self.category)
            if not os.path.exists(folder):
                os.makedirs(folder)
            with open(os.path.join(folder, schem_name), 'wb') as f:
                f.write(response.body)
    def after_login(self, response):
        print('Logged in')
        for i in range(10):
            yield scrapy.Request(url="https://www.minecraft-schematics.com/category/houses-and-shops/{}/".format(i), callback=self.parse)
        # for i in range(5):
        #     yield scrapy.Request(url="https://www.minecraft-schematics.com/category/towers/{}/".format(i), callback=self.parse)
        # for i in range(5):
        #     yield scrapy.Request(url="https://www.minecraft-schematics.com/category/towns/{}/".format(i), callback=self.parse)
        # for i in range(5):
        #     yield scrapy.Request(url="https://www.minecraft-schematics.com/category/temples/{}/".format(i), callback=self.parse)
        # for i in range(5):
        #     yield scrapy.Request(url="https://www.minecraft-schematics.com/category/miscellaneous/{}/".format(i), callback=self.parse)
        # for i in range(5):
        #     yield scrapy.Request(url="https://www.minecraft-schematics.com/category/gardens/{}/".format(i), callback=self.parse)
        # for i in range(5):
        #     yield scrapy.Request(url="https://www.minecraft-schematics.com/category/ground-vehicles/{}/".format(i), callback=self.parse)