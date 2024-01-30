from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    dishes_cooked = models.IntegerField(default=0)

    def str(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=255)
    products = models.ManyToManyField(Product, through='RecipeProduct')

    def str(self):
        return self.name


class RecipeProduct(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    weight = models.IntegerField()

    def str(self):
        return f"{self.recipe.name} - {self.product.name}"
