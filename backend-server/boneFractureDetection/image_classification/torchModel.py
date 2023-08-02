import torch

from boneFractureDetection.image_classification.CNN import CNN
from boneFractureDetection.image_classification.imageProcessing import cvImageToTorch

torch.set_float32_matmul_precision("medium")
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
modelPath = 'D:/CP/BoneFractureDetection/backend-server/boneFractureDetection/image_classification/model/modelV3.ckpt'

def getPredictions(imageBytes):
    if torch.cuda.is_available():
        model = CNN.load_from_checkpoint(modelPath,
                                         map_location=torch.device('cuda'))
    else:
        model = CNN.load_from_checkpoint(modelPath,
                                         map_location=torch.device('cpu'))

    model.eval()

    image = cvImageToTorch(imageBytes=imageBytes)

    with torch.no_grad():
        output = model(image.to(device)).to(device)

    predicted_class = torch.argmax(output, dim=1)

    return predicted_class

# def test():
# csv_path = "/kaggle/input/csv-file/valid_XR_FINGER_HAND_WRIST.csv"
# data = pd.read_csv(csv_path)
# print(f'date size = {len(data)}')
# countTrue = 0
# arrayOfTrue = []
#
# model.eval()
# for i in range(len(data)):
#
#     if i % 100 == 0:
#         print(f'{i}/{len(data)}')
#
#     image_path = os.path.join("/kaggle/input/mura-v11/", data.iloc[i, 0])
#     label = data.iloc[i, 1]
#
#
#     if predicted_class == label:
#         countTrue += 1
#         arrayOfTrue.append(image_path)
#
# print(f'count True: {countTrue}')
# print(f'{countTrue / len(data)}')
#
# print(*arrayOfTrue, sep="\n")
