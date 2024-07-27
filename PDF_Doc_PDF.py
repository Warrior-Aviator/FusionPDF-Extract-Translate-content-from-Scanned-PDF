import convertapi

convertapi.api_secret = '4OYbALQ2RREClhvm'

#Specify the file path here
doc = 'D:\College\Sem-6\Mini Project\VTU Demo 2'

convertapi.convert('docx', {
    'File': f'op1.pdf' 
}, from_format = 'pdf').save_files('documents.docx')

#convertapi.convert('pdf', {
#    'File': f'{doc}.docx' 
#}, from_format = 'docx').save_files('documents.txt')
