def setup(config):
  os.environ("OPENAI_API_KEY") = config["OPENAI_API_KEY"]
  os.environ("pdf_file") = config["pdf_file"]
  
def run(msg):
  
