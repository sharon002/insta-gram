from django.test import TestCase
from .models import Profile, Image, Comments
from django.contrib.auth.models import User


class ProfileTestClass(TestCase):
    """
    Test profile class and its functions
    """
    
    def setUp(self):

        # creating an new profile
        self.profile = Profile(bio='This is my bio', dp='name.jpg')

    def test_instance(self):
        self.assertTrue(isinstance(self.profile, Profile))

    def test_save_method(self):
        """
        Function to test that profile is being saved
        """
        self.profile.save_profile()
        profiles = Profile.objects.all()
        self.assertTrue(len(profiles) > 0)

    def test_delete_method(self):
        """
        Function to test that a profile can be deleted
        """
        self.profile.save_profile()
        self.profile.del_profile()

    def test_update_method(self):
        """
        Function to test that a profile's details can be updated
        """
        self.profile.save_profile()
        new_profile = Profile.objects.filter(
            bio='This is my bio').update(bio='Now this is the real bio')
        profiles = Profile.objects.get(bio='Now this is the real bio')
        self.assertTrue(profiles.bio, 'Now this is the real bio')


class ImageTestClass(TestCase):
    """
    Test Image class and its functions
    """

    def setUp(self):
        # creating an new profile and saving it
        self.profile = Profile(bio='This is my bio')
        self.profile.save_profile()
        # creating an new image
        self.image = Image(post='test.jpg', caption='Caption',
                           posted_on='Monday', profile=self.profile)

    def test_instance(self):
        self.assertTrue(isinstance(self.image, Image))

    def test_save_method(self):
        """
        Function to test that image is being saved
        """
        self.image.save_img()
        images = Image.objects.all()
        self.assertTrue(len(images) > 0)

    def test_delete_method(self):
        """
        Function to test that an image can be deleted
        """
        self.image.save_img()
        self.image.del_img()

    def test_update_method(self):
        """
        Function to test that an image's details can be updated
        """
        self.image.save_img()
        new_image = Image.objects.filter(
            caption='caption ').update(caption='caption')
        images = Image.objects.get(caption='caption')
        self.assertTrue(images.caption, 'caption')


class CommentsTestClass(TestCase):
    """
    Test Comments class and its functions
    """

    def setUp(self):

         # creating an new profile and saving it
        self.profile = Profile(bio='This is my bio')
        self.profile.save_profile()
        # creating an new image and saving it
        self.image = Image(post='test.jpg', caption='caption',
                           posted_on='Monday', profile=self.profile)
        self.image.save_img()
        # creating a new comment and saving it
        self.comm = Comments(
            comment='lol', posted_on='Monday', image=self.image)

    def test_instance(self):
        self.assertTrue(isinstance(self.comm, Comments))

    def test_save_method(self):
        """
        Function to test that a comment is being saved
        """
        self.comm.save_comm()
        feedback = Comments.objects.all()
        self.assertTrue(len(feedback) > 0)

    def test_delete_method(self):
        """
        Function to test that a comment can be deleted
        """
        self.comm.save_comm()
        self.comm.del_comm()

    def test_get_comment_by_image_id(self):
        """
        Function to test if you can get comments based on the image_id
        """
        self.comm.save_comm()
        this_comm = self.comm.get_comments_by_image_id(self.comm.image_id)
        comments = Comments.objects.get(id=self.comm.image_id)
        self.assertTrue(this_comm, comments)
