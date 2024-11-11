# eyJ1IjoicG9ydGFsLmFkbWluQGZha2VBZGRyZXNzLmNvbSIsInQiOiJzWG9ibU5iRDlmQnNmMERwSGJyOFBteUErNzd3ekxXWk5mU3M5MTE4MTFOaFlXRFA5VlNIazEyc0cyVEVhNmZnb0RIY2Z5RXAvYXByR2xqcHRsdi9MUT09In0=
import pysimio

def testAuth():
    api = pySimio("https://test.internal.simioportal.com:8443")
    api.authenticate("eyJ1IjoicG9ydGFsLmFkbWluQGZha2VBZGRyZXNzLmNvbSIsInQiOiJzWG9ibU5iRDlmQnNmMERwSGJyOFBteUErNzd3ekxXWk5mU3M5MTE4MTFOaFlXRFA5VlNIazEyc0cyVEVhNmZnb0RIY2Z5RXAvYXByR2xqcHRsdi9MUT09In0=")
    print(api.authToken)

if __name__ == "main":
    testAuth()