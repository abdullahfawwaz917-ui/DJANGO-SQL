from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse
from django.utils.html import escape

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def dictfetchone(cursor):
    """Mengubah satu hasil query menjadi dictionary."""
    columns = [col[0] for col in cursor.description]
    row = cursor.fetchone()

    if row is None:
        return None

    return dict(zip(columns, row))



def siswa_list(request):
    # eksekusi query sql -> narik data siswa
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, nama, umur, tgl_lahir, status_hadir, nilai_akhir
            FROM siswa
            ORDER BY id DESC
        """)
        # di masukan ke variabel
        data_siswa = dictfetchall(cursor)

    # sample  inputan pencarian
    search_text = 'Bekasi'

    # render file html disertai data tertentu
    return render(request, 'list.html', {
        'keyword': search_text,
        'data': data_siswa
    })


def siswa_detail(request, id):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT * FROM siswa
            WHERE id = %s
            """,
            [id]
        )
        siswa = dictfetchone(cursor)    

    return render(request, 'detail.html', {
        'siswa': siswa,
    })



def siswa_create(request):
    # cek request yg masuk, klo dia POST (submit)
    if request.method == 'POST':        
        # kumpulkan data dari request post
        nama = request.POST.get('nama', '').strip()
        umur = request.POST.get('umur', '').strip()
        tanggal_lahir = request.POST.get('tanggal_lahir', '').strip()
        status_hadir = request.POST.get('status_hadir', '').strip()
        status_hadir = request.POST.get('status_hadir')

        if status_hadir == 'hadir':
            status_hadir = True
        else:
            status_hadir = False

        nilai_akhir = request.POST.get('nilai_akhir', '').strip()
        # eksekusi query insert ke tabel siswa
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO siswa (nama, umur, tgl_lahir, status_hadir, nilai_akhir)
                VALUES (%s, %s, %s, %s, %s)
                """,
                [nama, umur, tanggal_lahir, status_hadir, nilai_akhir]
            )

        # klo berhasil maka redirect ke siswa list
        return redirect('siswa_list')
    

    # klo gk submit (GET)
    return render(request, 'form.html')

def siswa_update(request, id):

    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE siswa
                SET nama=%s,
                    umur=%s,
                    tgl_lahir=%s,
                    status_hadir=%s,
                    nilai_akhir=%s
                WHERE id=%s
            """, [
                request.POST['nama'],
                request.POST['umur'],
                request.POST['tgl_lahir'],
                request.POST['status_hadir'],
                request.POST['nilai_akhir'],
                id
            ])

        return redirect('siswa_list')

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT * FROM siswa
            WHERE id = %s
        """, [id])

        siswa = dictfetchone(cursor)

    return render(request, 'edit.html', {
        'siswa': siswa,
    })


def siswa_delete(request, id):

    if request.method == "POST":
        with connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM siswa
                WHERE id = %s
                """,
                [id]
            )

        return redirect('siswa_list')

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT * FROM siswa
            WHERE id = %s
            """,
            [id]
        )
        siswa = dictfetchone(cursor)

    return render(request, 'hapus.html', {
        'siswa': siswa
    })