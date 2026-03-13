import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from django.views.decorators.http import require_POST
from .models import Note, Category, Tag
from .forms import SignUpForm, NoteForm, CategoryForm


# ── Auth Views ──

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('note_list')
    else:
        form = SignUpForm()
    return render(request, 'notes/signup.html', {'form': form})


@login_required
def profile(request):
    notes_count = Note.objects.filter(user=request.user, is_trashed=False).count()
    categories_count = Category.objects.filter(user=request.user).count()
    return render(request, 'notes/profile.html', {
        'notes_count': notes_count,
        'categories_count': categories_count,
    })


# ── Note CRUD Views ──

@login_required
def note_list(request):
    notes = Note.objects.filter(user=request.user, is_trashed=False)

    # Search
    query = request.GET.get('q', '')
    if query:
        notes = notes.filter(Q(title__icontains=query) | Q(body__icontains=query))

    # Filter by category
    category_id = request.GET.get('category')
    if category_id:
        notes = notes.filter(category_id=category_id)

    # Filter by tag
    tag_id = request.GET.get('tag')
    if tag_id:
        notes = notes.filter(tags__id=tag_id)

    categories = Category.objects.filter(user=request.user)
    tags = Tag.objects.filter(user=request.user)

    return render(request, 'notes/note_list.html', {
        'notes': notes,
        'categories': categories,
        'tags': tags,
        'query': query,
        'selected_category': category_id,
        'selected_tag': tag_id,
    })


@login_required
def note_detail(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user, is_trashed=False)
    return render(request, 'notes/note_detail.html', {'note': note})


@login_required
def note_create(request):
    if request.method == 'POST':
        form = NoteForm(request.POST, user=request.user)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            _save_tags(note, form.cleaned_data.get('tags_input', ''), request.user)
            return redirect('note_list')
    else:
        form = NoteForm(user=request.user)
    categories = Category.objects.filter(user=request.user)
    return render(request, 'notes/note_form.html', {'form': form, 'categories': categories})


@login_required
def note_edit(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note, user=request.user)
        if form.is_valid():
            note = form.save()
            _save_tags(note, form.cleaned_data.get('tags_input', ''), request.user)
            return redirect('note_detail', pk=note.pk)
    else:
        form = NoteForm(instance=note, user=request.user)
    categories = Category.objects.filter(user=request.user)
    return render(request, 'notes/note_form.html', {'form': form, 'note': note, 'categories': categories})


@login_required
@require_POST
def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    note.is_trashed = True
    note.save()
    return redirect('note_list')


@login_required
@require_POST
def note_pin(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    note.is_pinned = not note.is_pinned
    note.save()
    return redirect('note_list')


# ── Trash Views ──

@login_required
def trash_list(request):
    notes = Note.objects.filter(user=request.user, is_trashed=True).order_by('-updated_at')
    return render(request, 'notes/trash.html', {'notes': notes})


@login_required
@require_POST
def note_restore(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user, is_trashed=True)
    note.is_trashed = False
    note.save()
    return redirect('trash_list')


@login_required
@require_POST
def note_permanent_delete(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user, is_trashed=True)
    note.delete()
    return redirect('trash_list')


# ── Category Views ──

@login_required
def category_manage(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            cat = form.save(commit=False)
            cat.user = request.user
            cat.save()
            return redirect('category_manage')
    else:
        form = CategoryForm()
    categories = Category.objects.filter(user=request.user)
    return render(request, 'notes/categories.html', {'form': form, 'categories': categories})


@login_required
@require_POST
def category_delete(request, pk):
    cat = get_object_or_404(Category, pk=pk, user=request.user)
    cat.delete()
    return redirect('category_manage')


# ── Auto Save (AJAX) ──

@login_required
@require_POST
def note_autosave(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    data = json.loads(request.body)
    note.title = data.get('title', note.title)
    note.body = data.get('body', note.body)
    note.save()
    return JsonResponse({'status': 'saved', 'updated_at': note.updated_at.isoformat()})


# ── Export Views ──

@login_required
def note_export_txt(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    response = HttpResponse(
        f"{note.title}\n{'=' * len(note.title)}\n\n{note.body}\n\nCreated: {note.created_at}\nUpdated: {note.updated_at}",
        content_type='text/plain',
    )
    response['Content-Disposition'] = f'attachment; filename="{note.title}.txt"'
    return response


@login_required
def note_export_md(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    response = HttpResponse(
        f"# {note.title}\n\n{note.body}\n\n---\n*Created: {note.created_at}*  \n*Updated: {note.updated_at}*",
        content_type='text/markdown',
    )
    response['Content-Disposition'] = f'attachment; filename="{note.title}.md"'
    return response


# ── Helpers ──

def _save_tags(note, tags_input, user):
    note.tags.clear()
    if tags_input:
        tag_names = [t.strip() for t in tags_input.split(',') if t.strip()]
        for name in tag_names:
            tag, _ = Tag.objects.get_or_create(name=name, user=user)
            note.tags.add(tag)
