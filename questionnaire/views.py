from django.shortcuts import render
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.lib.units import cm
from .models import Question
from datetime import datetime
import os
from django.conf import settings
# Create your views here.

import wikipedia
from django.shortcuts import render
from .models import Question

def poser_question(request):
    reponse = None
    question_text = ""

    if request.method == "POST":
        question_text = request.POST.get("question")
        try:
            wikipedia.set_lang("fr")
            reponse = wikipedia.summary(question_text, sentences=3, auto_suggest=True)
        except Exception:
            reponse = "Désolé, je n'ai pas trouvé de réponse à cette question."

        # ✅ Sauvegarder dans la base de données
        Question.objects.create(texte=question_text, reponse=reponse)

    return render(request, "questionnaire/poser_question.html", {
        "reponse": reponse,
        "question": question_text,
    })



def poser_question(request):
    reponse = None
    question_text = ""

    if request.method == "POST":
        question_text = request.POST.get("question")
        try:
            wikipedia.set_lang("fr")
            reponse = wikipedia.summary(question_text, sentences=3, auto_suggest=True)
        except Exception:
            reponse = "Désolé, je n'ai pas trouvé de réponse à cette question."

        # ✅ Sauvegarde automatique
        Question.objects.create(texte=question_text, reponse=reponse)

    return render(request, "questionnaire/poser_question.html", {
        "reponse": reponse,
        "question": question_text,
    })


# ✅ Nouvelle vue : afficher toutes les questions enregistrées
def historique(request):
    questions = Question.objects.order_by('-date_ajout')  # tri par date décroissante
    return render(request, "questionnaire/historique.html", {"questions": questions})


def telecharger_pdf(request):
    # --- Configuration du PDF ---
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="questions_reponses.pdf"'

    # Création du document
    doc = SimpleDocTemplate(
        response,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm
    )

    # --- Définition des styles ---
    styles = getSampleStyleSheet()
    titre_principal = ParagraphStyle(
        'TitrePrincipal',
        parent=styles['Heading1'],
        fontSize=22,
        alignment=TA_CENTER,
        textColor=colors.white,
        spaceAfter=20,
        leading=24
    )

    sous_titre = ParagraphStyle(
        'SousTitre',
        parent=styles['Heading2'],
        fontSize=14,
        alignment=TA_CENTER,
        textColor=colors.white,
        spaceAfter=20
    )

    info_style = ParagraphStyle(
        'Info',
        parent=styles['Normal'],
        fontSize=12,
        alignment=TA_CENTER,
        leading=18
    )

    normal_justifie = ParagraphStyle(
        'NormalJustifie',
        parent=styles['Normal'],
        fontSize=11,
        alignment=TA_JUSTIFY,
        leading=15
    )

    date_style = ParagraphStyle(
        'Date',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.gray,
        alignment=TA_CENTER
    )

    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_CENTER,
        textColor=colors.gray
    )

    # --- Liste des éléments à inclure ---
    elements = []

    # ========== PAGE DE GARDE ==========

    # Bandeau bleu UQAR
    def draw_header(canvas, doc):
        canvas.saveState()
        width, height = A4
        bandeau_height = 5 * cm
        canvas.setFillColor(colors.HexColor("#1a73e8"))
        canvas.rect(0, height - bandeau_height, width, bandeau_height, fill=1)

        # Logo UQAR
        logo_path = os.path.join(settings.BASE_DIR, 'questionnaire/static/images/téléchargement.jpeg')
        if os.path.exists(logo_path):
            canvas.drawImage(logo_path, 2 * cm, height - 4.5 * cm, width=3.5 * cm, preserveAspectRatio=True, mask='auto')

        # Titre sur bandeau
        canvas.setFont("Helvetica-Bold", 22)
        canvas.setFillColor(colors.white)
        canvas.drawCentredString(width / 2, height - 2.5 * cm, "Projet de Mémoire")
        canvas.setFont("Helvetica-Bold", 14)
        canvas.drawCentredString(width / 2, height - 3.8 * cm, "Application d’Aide à la Préparation de Soutenance")

        canvas.restoreState()

    # Ajouter espace après bandeau
    elements.append(Spacer(1, 6 * cm))

    # Informations centrées
    elements.append(Paragraph("<b>Réalisé par :</b> Elhadji Ousmane Faye", info_style))
    elements.append(Paragraph("<b>Sous la supervision de :</b> [Nom du superviseur]", info_style))
    elements.append(Spacer(1, 0.5 * cm))
    elements.append(Paragraph(f"<b>Date :</b> {datetime.now().strftime('%d/%m/%Y')}", info_style))
    elements.append(Spacer(1, 5 * cm))
    elements.append(Paragraph("Université du Québec à Rimouski (UQAR)", footer_style))
    elements.append(PageBreak())

    # ========== PAGE DE CONTENU ==========
    elements.append(Paragraph("Historique des Questions et Réponses", ParagraphStyle(
        'TitreContenu',
        parent=styles['Heading1'],
        fontSize=18,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#1a73e8"),
        spaceAfter=20
    )))

    questions = Question.objects.order_by('-date_ajout')

    for q in questions:
        question_text = f"<b>Question :</b> {q.texte}"
        reponse_text = f"<b>Réponse :</b> {q.reponse or 'Aucune réponse trouvée.'}"
        date_text = f"<i>Date :</i> {q.date_ajout.strftime('%d/%m/%Y %H:%M')}"

        data = [
            [Paragraph(question_text, normal_justifie)],
            [Paragraph(reponse_text, normal_justifie)],
            [Paragraph(date_text, date_style)],
        ]

        table = Table(data, colWidths=[16 * cm])
        table.setStyle(TableStyle([
            ('BOX', (0, 0), (-1, -1), 1.2, colors.HexColor("#1a73e8")),
            ('BACKGROUND', (0, 0), (-1, 0), colors.whitesmoke),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
        ]))

        elements.append(table)
        elements.append(Spacer(1, 0.8 * cm))

    # ========== PIED DE PAGE (PAGINATION) ==========
    def header_footer(canvas, doc):
        canvas.saveState()
        width, height = A4
        page_num = doc.page
        canvas.setFont("Helvetica-Oblique", 9)
        canvas.setFillColor(colors.gray)
        canvas.drawCentredString(width / 2, 1.5 * cm, f"Page {page_num}")
        canvas.restoreState()

    # Génération du document complet
    doc.build(elements, onFirstPage=draw_header, onLaterPages=header_footer)

    return response