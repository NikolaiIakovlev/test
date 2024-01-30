from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.shortcuts import render
from .models import Recipe, Product, RecipeProduct
from django.views.decorators.cache import cache_page


def add_product_to_recipe(request):
    recipe_id = request.GET.get('recipe_id')
    product_id = request.GET.get('product_id')
    weight = request.GET.get('weight')

    recipe = get_object_or_404(Recipe, id=recipe_id)
    product = get_object_or_404(Product, id=product_id)

    recipe_product, created = RecipeProduct.objects.get_or_create(recipe=recipe, product=product)
    recipe_product.weight = weight
    recipe_product.save()

    return HttpResponse(f"Product added to recipe {recipe_id}")


def cook_recipe(request):
    recipe_id = request.GET.get('recipe_id')
    recipe = get_object_or_404(Recipe, id=recipe_id)

    for recipe_product in recipe.recipeproduct_set.all():
        product = recipe_product.product
        product.dishes_cooked += 1
        product.save()

    return HttpResponse(f"Recipe {recipe_id} cooked")


@cache_page(60 * 15)
def show_recipes_without_product(request):
    product_id = request.GET.get('product_id')
    product = get_object_or_404(Product, id=product_id)

    recipes_without_product = Recipe.objects.exclude(
        recipeproduct__product=product)
    recipes_less_than_10g = RecipeProduct.objects.filter(
        product=product, weight__lt=10).values_list('recipe', flat=True)

    context = {
        'recipes_without_product': recipes_without_product,
        'recipes_less_than_10g': recipes_less_than_10g,
    }

    return render(request, 'recipes_without_product.html', context)