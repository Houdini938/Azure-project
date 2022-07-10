import os
from azure.storage.blob import BlobServiceClient
from flask import Flask, request, redirect

app = Flask(__name__)

connect_str = os.getenv('AZURE_STORAGE_CONNECTION_KEY') # récupérer la clé de connexion à partir de la variable d'environnement
container_name = "photosstorageapp" # nom du conteneur dans lequel les images seront stockées dans le compte de stockage

cog_key = '73cc2fcaaa404d10a6903b13a0437c8e'
cog_endpoint = 'https://tag-language.cognitiveservices.azure.com/'

computervision_client = ComputerVisionClient(cog_endpoint, CognitiveServicesCredentials(cog_key))


blob_service_client = BlobServiceClient.from_connection_string(conn_str=connect_str) # créer un client de service blob pour interagir avec le compte de stockage
try:
    container_client = blob_service_client.get_container_client(container=container_name) # faire interagir le client conteneur avec le conteneur dans lequel les images seront stockées
    container_client.get_container_properties() # obtenir les propriétés du conteneur pour forcer la levée d'une exception si le conteneur n'existe pas
except Exception as e:
    print(e)
    print("Creating container...")
    container_client = blob_service_client.create_container(container_name) # créer un conteneur dans le compte de stockage s'il n'existe pas
 
@app.route("/")
def view_photos():
    blob_items = container_client.list_blobs() # lister tous les blobs du conteneur

    img_html = "<div style='display: flex; justify-content: space-between; flex-wrap: wrap;'>"

    for blob in blob_items:
        blob_client = container_client.get_blob_client(blob=blob.name) # obtenir le client blob pour interagir avec le blob et obtenir l'URL du blob
        img_html += "<img src='{}' width='auto' height='200' style='margin: 0.5em 0;'/>".format(blob_client.url) # obtenir l'url blob et l'ajouter au html
    
    img_html += "</div>"

    # retourner le html avec les images

    return """
    <head>
    <!-- CSS uniquement -->
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
    </head>
    <body>
        <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
            <div class="container">
                <a class="navbar-brand" href="/">Photos App</a>
            </div>
        </nav>
        <div class="container">
            <div class="card" style="margin: 1em 0; padding: 1em 0 0 0; align-items: center;">
                <h3>Upload new File</h3>
                <div class="form-group">
                    <form method="post" action="/upload-photos" 
                        enctype="multipart/form-data">
                        <div style="display: flex;">
                            <input type="file" accept=".png, .jpeg, .jpg, .gif" name="photos" multiple class="form-control" style="margin-right: 1em;">
                            <input type="submit" class="btn btn-primary">
                        </div>
                    </form>
                </div> 
            </div>
        
     """+ img_html + "</div></body>"

#flask endpoint pour upload une photo
@app.route("/upload-photos", methods=["POST"])
def upload_photos():
    filenames = ""

    for file in request.files.getlist("photos"):
        try:
            container_client.upload_blob(file.filename, file) # upload le fichier dans le conteneur en utilisant le nom de fichier comme nom de blob
            filenames += file.filename + "<br /> "
        except Exception as e:
            print(e)
            print("ignore les noms de fichiers en double") # ignorer les noms de fichiers en double
        
    return redirect('/') 
 

print("===== Detect Brands =====")

image_path = 'https://tag-language.cognitiveservices.azure.com/'
image_stream = open(image_path, "rb")
img = Image.open(image_path)

# Select the visual feature(s) you want
features = ["brands"]

# Call API with image
# detect_objects_results = computervision_client.analyze_image_in_stream(image_stream, features)

# Print detection results with bounding box and confidence score
print("Detecting brands in local image: ")
if len(detect_objects_results.brands) == 0:
    print("No brands detected.")
else:
    for brand in detect_objects_results.brands:
        print("'{}' brand detected with confidence {:.1f}% at location {}, {}, {}, {}".format( \
        brand.name, brand.confidence * 100, brand.rectangle.x, brand.rectangle.x + brand.rectangle.w, \
        brand.rectangle.y, brand.rectangle.y + brand.rectangle.h))

plt.imshow(img)







