from django.db import models

# Create your models here.
max_length = 100


class Character(models.Model):

    # Names
    first_name = models.CharField(max_length=max_length)
    middle_name = models.CharField(max_length=max_length)
    last_name = models.CharField(max_length=max_length)

    # Demographic details
    gender = models.CharField(max_length=max_length)
    age = models.PositiveSmallIntegerField()
    ethnicity = models.CharField(max_length=max_length)
    occupation = models.CharField(max_length=max_length)

    # Physical details
    hair_color = models.CharField(max_length=max_length)
    eye_color = models.CharField(max_length=max_length)
    height = models.CharField(max_length=max_length)
    body_type = models.CharField(max_length=max_length)

    # Generate MBTI personality type combinations
    mbti_choices = []
    for e_i in ['E', 'I']:
        for n_s in ['N', 'S']:
            for f_t in ['F', 'T']:
                for j_p in ['J', 'P']:
                    mbti_choices.append(e_i + n_s + f_t + j_p)

    # Generate enneagram types 1 through 9
    enneagram_choices = [num + 1 for num in range(9)]

    mbti_personality = models.CharField(choices=mbti_choices, max_length=4)
    enneagram_personality = models.PositiveSmallIntegerField(choices=enneagram_choices)

    # Long character description
    description = models.TextField()


class Plot(models.Model):
    title = models.CharField(max_length=200)
    synopsis = models.TextField()
    # ... other fields

class World(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    # ... other fields

class Scene(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    plot = models.ForeignKey(Plot, on_delete=models.CASCADE)
    # ... other fields