from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# Create your models here.

"""Helps Django to create User with our implementation of managing User"""
class UserManager ( BaseUserManager ) :

	"""Creates a new User in the System"""
	def create_user ( self, email, name, password = None ) :
		# Check whether new User request contains Email Address or not.
		# This is necessary since 'email' will be used as the Primary Key in our DB.
		if not email :
			raise ValueError ( "User must have Email Address" )

		# Normalize the Email Address so that upon entering Email Address with case insensitive,
		# it will be formatted to same format.
		email = self.normalize_email ( email )

		# Create an instance of User.
		user = self.model ( email = email, name = name )

		# Store the Password in Encrypted Form so that password is not clearly stored in DB.
		user.set_password ( password )

		# Save the User to DB.
		user.save ( using = self.db )
		return user

	"""Creates Super User in the System"""
	def create_super_user ( self, name, email, password ) :
		# Create a normal user.
		user = self.create_user ( email, name, password )

		# Specify this user that it is a Super User.
		user.is_superuser = True

		# Specify this user that it is a Staff.
		user.staff = True

		# Return the User.
		return user

"""Represent a User in our System"""
class User ( AbstractBaseUser, PermissionsMixin ) :
	email = models.EmailField ( max_length = 255, unique = True )
	name = models.CharField ( max_length = 50 )
	active = models.BooleanField ( default = True )
	staff = models.BooleanField ( default = False )

	objects = UserManager ()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = [ 'name' ]

	"""Gets the Name of User"""
	def get_name ( self ) :
		return self.name

	"""Gets the Email of User"""
	def get_email ( self ) :
		return self.email

	def __str__ ( self ) :
		return self.get_email ()