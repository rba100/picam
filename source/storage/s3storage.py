import boto3
import os

class S3Storage:
  def __init__(self, bucketName="rba-picam"):
    self._bucketName = bucketName
    self._s3 = boto3.resource('s3')
    pass

  def move(self, filePath, targetPath):
    self.copy(targetPath, filePath)
    os.remove(filePath)

  def copy(self, filePath, targetPath):
    self._s3.Bucket(self._bucketName).upload_file(filePath, targetPath)
