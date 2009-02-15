from distutils.core import setup

data = []
data.extend([
    'templates/admin/correx/*.html',
    'fixtures/*.json',
    'tests/fixtures/*.json'
    ]
)

setup(name="django-correx",
      description="A set of models and template tags for pulling in lists of content changes across applications.",
      version='0.21',
      author='Ben Welsh',
      author_email='palewire@palewire.com',
      url="http://www.palewire.com",
      packages=[
         "correx", 
         "correx.fixtures",
         "correx.templatetags",
         "correx.tests",
         "correx.tests.fixtures",
         "correx.tests.unittests",],
     package_data={ 'correx': data },
    )