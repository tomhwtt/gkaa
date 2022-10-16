from django.shortcuts import render, HttpResponse, HttpResponseRedirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.db.models import Q

from app.decorators import view_login_required, edit_login_required

from decouple import config
import boto3

from app.models import Gallery, GalleryImage
from utils.utils import create_url_code

@edit_login_required
def gallery_list(request):

    gallery_set = Gallery.objects.all()

    context = {
        'gallery_set': gallery_set
    }

    return render(request, 'app/gallery/gallery_list.html', context)

@edit_login_required
def gallery_detail(request,pk):

    gallery = get_object_or_404(Gallery,pk=pk)

    # create a more images list
    holder_set = gallery.galleryimageholder_set.all().select_related(
        'galleryimage',
        'gallery'
    )[:24]

    image_list = []

    for h in holder_set:

        image_obj = {
            'id': h.id,
            'image_id': h.galleryimage.id,
            'uuid': h.galleryimage.uuid,
            'slug': h.gallery.slug,
            'src': h.galleryimage.grid_src()
        }

        image_list.append(image_obj)

    context = {
        'gallery': gallery,
        'image_list': image_list,
        'num_images': len(image_list)
    }

    return render(request, 'app/gallery/gallery_detail.html', context)


@edit_login_required
def galleryimage_detail(request,pk):

    galleryimage = get_object_or_404(GalleryImage,pk=pk)

    # later this will update the entire image
    if request.method == 'POST':

        # set the Amazon S3 Client
        client = boto3.client('s3',
            aws_access_key_id=config('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY')
            )

        # set the posted file
        file = request.FILES['image']

        # set the current image name
        current_name = galleryimage.old_name

        # remove the current image from AWS
        client.delete_object(
            Bucket='gkaa-imgix',
            Key='images/ogallery/' + galleryimage.old_name
            )

        # create a new image name
        # this code creates a 12 character short code
        name = create_url_code() + '.jpg'

        # we do not have ACL = public-read here because
        # this folder is locked down in AWS
        bucket = client.put_object(
            Bucket ='gkaa-imgix',
            Body = file,
            Key = 'images/ogallery/' + name,
            ContentType = file.content_type,
        )

        # update the image with the new image name
        galleryimage.old_name = name
        galleryimage.save()

        # update the GalleryImage
        return HttpResponseRedirect(
            reverse('app:galleryimage-detail', args=(galleryimage.id,)))

    # if NOT post
    else:

        context = {
            'image': galleryimage
        }

        return render(request, 'app/gallery/galleryimage_detail.html', context)
