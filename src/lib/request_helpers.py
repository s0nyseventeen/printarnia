def get_img_info(request):
    return request.files.get('image'), request.form.get('image_description')
