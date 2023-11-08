from test.tests import remove

if __name__ == '__main__':    try: os.remove("recipes.db")    except: pass    FlaskProjectTest().run_tests()    try: os.remove("recipes.db")    except: pass