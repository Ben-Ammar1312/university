from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from student.models import Student_Subject, Student, Teacher, Classes, Subject
from django.conf import settings
import os

def get_timetable_file(class_name):
    timetable_path = 'timetables'  # Change this line
    timetable_files = os.listdir(os.path.join(settings.BASE_DIR, 'student', 'static', timetable_path))  # Change this line

    for file in timetable_files:
        if class_name in file:
            return os.path.join(timetable_path, file)

    return None



def home(request):
    if request.user.is_authenticated:
        if request.user.is_student:
            return redirect('student_resultat')
        elif request.user.is_teacher:
            return redirect('teacher_home')
    return render(request, 'home.html')


@login_required
@user_passes_test(lambda u: u.is_student)
def student_resultat(request):
    student = Student.objects.filter(student_profile=request.user).first()
    student_subjects = Student_Subject.objects.filter(student=student)
    all_subjects = student.student_classes.matiere.all()

    subject_grades = {}

    for subject in all_subjects:
        subject_grades[subject.libelle] = {
            'note_ds': None,
            'note_ex': None,
            'moyenne': None,
        }

    for subject_grade in student_subjects:
        subject_grades[subject_grade.subject.libelle] = {
            'note_ds': subject_grade.note_ds,
            'note_ex': subject_grade.note_ex,
            'moyenne': subject_grade.moyenne,
        }

    return render(request, 'student_homepage.html', {'subject_grades': subject_grades, 'user': student})



@login_required
@user_passes_test(lambda u: u.is_teacher)
def teacher_home(request):
    query_set = Teacher.objects.filter(profile=request.user).first()
    teacher_classes = query_set.teacher_class.all().values_list(
        'libelle', flat=True)
    return render(request, 'teacher_homepage.html', {'cla': teacher_classes, 'classes': ['CPI-1', 'CPI-2', 'TIC-A', 'TIC-B', 'TIC-C', 'TIC-D', 'TIC-E', 'TIC-F', 'TIC-G', 'TIC-K', 'GLSI', 'SSIR', 'DSEN', 'DMWM']})


@login_required
@user_passes_test(lambda u: u.is_teacher)
def teacher_matiere(request):
    query_set = Teacher.objects.filter(profile=request.user).first()
    teacher_subjects = query_set.teacher_subject.all().values_list('libelle', flat=True)
    query_set2 = Classes.objects.filter(
        libelle=request.GET.get('classe')).first()
    query_set2 = query_set2.matiere.all().values_list('libelle', flat=True)
    return render(request, 'matieres.html', {'subs': teacher_subjects, 'classe': request.GET.get('classe'), 'all': query_set2})


@login_required
@user_passes_test(lambda u: u.is_teacher)
def teacher_note(request, classe, subject):
    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('note_ds_') and value:
                student_id = int(key[8:])
                note_ds = float(value)
                student = Student.objects.get(id=student_id)
                subject1 = Subject.objects.get(libelle=subject)
                student_subject, created = Student_Subject.objects.get_or_create(
                    student=student, subject=subject1)
                student_subject.note_ds = note_ds
                student_subject.save()
            if key.startswith('note_ex_') and value:
                student_id = int(key[8:])
                note_ex = float(value)
                student = Student.objects.get(id=student_id)
                subject1 = Subject.objects.get(libelle=subject)
                student_subject, created = Student_Subject.objects.get_or_create(
                    student=student, subject=subject1)
                student_subject.note_ex = note_ex
                student_subject.save()
        return redirect('teacher_note', classe=classe, subject=subject)
    else:
        subj = Subject.objects.filter(
            libelle=subject).first()
        id = Classes.objects.filter(libelle=classe).first()
        query_set = Student.objects.filter(student_classes=id.id)
        query_set2 = Student_Subject.objects.filter(
            subject=subj, student__in=query_set).all()
        notes_dict = {}
        for student_subject in query_set2:
            student_name = student_subject.student.student_profile.username
            notes_dict[student_name] = [
                student_subject.note_ds, student_subject.note_ex]
        return render(request, 'teacher_note.html', {'students': query_set, 'classe': classe, 'subject': subject, 'notes': notes_dict})


@login_required
@user_passes_test(lambda u: u.is_student)
def student_emploi(request):
    student = Student.objects.get(student_profile=request.user)
    timetable_file = get_timetable_file(student.student_classes.libelle)
    context = {
        'timetable_file': timetable_file,
    }
    return render(request, 'emploi.html', context)
