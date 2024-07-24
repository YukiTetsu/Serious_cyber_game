import pygame
import sys
import os  # Importe le module pour les opérations système
import glob  # Importe le module pour la recherche de chemins de fichiers
import hashlib

pygame.init()

# Load the click sound and background music
click_sound = pygame.mixer.Sound('sound/clicksound.wav')
pygame.mixer.music.load('sound/main_song.mp3')
pygame.mixer.music.play(-1)  # Play the background music in a loop

# Load background images with the correct extensions
main_back = pygame.image.load('Picture/main_back.jpg')
option_back = pygame.image.load('Picture/option_back.png')

res = (1720, 1000)
screen = pygame.display.set_mode(res)

color = (255, 255, 255)
color_light = (170, 170, 170)
color_dark = (100, 100, 100)

width = screen.get_width()
height = screen.get_height()

smallfont = pygame.font.SysFont('Corbel', 35)

text_quit = smallfont.render('Quitter', True, color)
text_options = smallfont.render('Options', True, color)
text_play = smallfont.render('Jouer', True, color)
text_resolution = smallfont.render('Resolution', True, color)
text_volume = smallfont.render('Volume', True, color)
text_level_1 = smallfont.render('Niveau 1', True, color)
text_level_2 = smallfont.render('Niveau 2', True, color)
text_level_3 = smallfont.render('Niveau 3', True, color)

class Button:
    def __init__(self, x, y, width, height, color_light, color_dark, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color_light = color_light
        self.color_dark = color_dark
        self.text = text

    def draw(self, screen):
        mouse = pygame.mouse.get_pos()
        if self.x <= mouse[0] <= self.x + self.width and self.y <= mouse[1] <= self.y + self.height:
            pygame.draw.rect(screen, self.color_light, [self.x, self.y, self.width, self.height])
        else:
            pygame.draw.rect(screen, self.color_dark, [self.x, self.y, self.width, self.height])
        screen.blit(self.text, (self.x + (self.width - self.text.get_width()) // 2, self.y + (self.height - self.text.get_height()) // 2))

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if self.x <= mouse[0] <= self.x + self.width and self.y <= mouse[1] <= self.y + self.height:
                click_sound.play()  # Play the click sound
                return True
        return False

class Slider:
    def __init__(self, x, y, width, height, min_val, max_val):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.min_val = min_val
        self.max_val = max_val
        self.value = min_val
        self.slider_color = (200, 200, 200)
        self.bar_color = (100, 100, 100)
        self.dragging = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.bar_color, [self.x, self.y, self.width, self.height])
        pygame.draw.rect(screen, self.slider_color, [self.x + (self.value - self.min_val) / (self.max_val - self.min_val) * self.width - self.height // 2, self.y - self.height // 2, self.height, self.height * 2])

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if self.x <= mouse[0] <= self.x + self.width and self.y <= mouse[1] <= self.y + self.height:
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                mouse = pygame.mouse.get_pos()
                self.value = (mouse[0] - self.x) / self.width * (self.max_val - self.min_val) + self.min_val
                if self.value < self.min_val:
                    self.value = self.min_val
                if self.value > self.max_val:
                    self.value = self.max_val

    def get_value(self):
        return self.value / self.max_val  # Returns value as a percentage (0 to 1)

class InputBox:
    def __init__(self, x, y, w, h, text='', is_password=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color_dark
        self.text = text
        self.is_password = is_password
        self.txt_surface = smallfont.render(self.text, True, self.color)
        self.active = False
        self.font = pygame.font.SysFont('Corbel', 20)  # Smaller font

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = color_light if self.active else color_dark
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    pass
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Render the text with masking for password fields
                display_text = '*' * len(self.text) if self.is_password else self.text
                self.txt_surface = self.font.render(display_text, True, self.color)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 2)
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def get_text(self):
        return self.text

# Main menu functions

def main_menu():
    play_button = Button(width / 2 - 70, height / 2 - 60, 140, 40, color_light, color_dark, text_play)
    options_button = Button(width / 2 - 70, height / 2, 140, 40, color_light, color_dark, text_options)
    quit_button = Button(width / 2 - 70, height / 2 + 60, 140, 40, color_light, color_dark, text_quit)

    main_back_rect = main_back.get_rect(center=(width // 2, height // 2))  # Center the background

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if play_button.is_clicked(event):
                level_selection()
            if options_button.is_clicked(event):
                options_menu()
            if quit_button.is_clicked(event):
                pygame.quit()
                sys.exit()

        screen.blit(main_back, main_back_rect.topleft)  # Draw the main menu background
        play_button.draw(screen)
        options_button.draw(screen)
        quit_button.draw(screen)

        pygame.display.update()

def options_menu():
    global screen, width, height
    # Création du slider pour le volume
    volume_slider = Slider(width / 2 - 70 + 20, height / 2 + 30, 140, 20, 0, 100)
    # Création du bouton pour revenir au menu principal
    back_button = Button(10, 10, 100, 40, color_light, color_dark, smallfont.render('Back', True, color))

    # Création du texte pour le titre "Modifier le son"
    volume_text = smallfont.render('Modifier le son', True, color)

    # Centre le fond des options
    option_back_rect = option_back.get_rect(center=(width // 2, height // 2))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if back_button.is_clicked(event):
                return
            volume_slider.handle_event(event)

        # Mise à jour du volume de la musique et du son de clic selon le slider
        volume = volume_slider.get_value()
        pygame.mixer.music.set_volume(volume)
        click_sound.set_volume(volume)

        # Dessiner le fond des options
        screen.blit(option_back, option_back_rect.topleft)
        # Dessiner le texte pour modifier le son
        screen.blit(volume_text, (width / 2 - volume_text.get_width() / 2 + 30, height / 2 - volume_text.get_height() - 0))
        # Dessiner le slider de volume
        volume_slider.draw(screen)
        # Dessiner le bouton de retour
        back_button.draw(screen)

        pygame.display.update()

class Email:
    def __init__(self, sender, subject, body, image):
        self.sender = sender
        self.subject = subject
        self.body = body
        self.image = image
        self.loaded_image = None

class EmailBox:
    def __init__(self, x, y, width, height, emails):
        self.rect = pygame.Rect(x, y, width, height)
        self.emails = emails
        self.selected_email = None
        self.correct_clicks = []
        self.target_coords = [(597, 40), (800, 40), (751, 537), (180, 400)]  # Coordinates for phishing indicators
        self.click_radius = 100  # Radius within which a click is considered correct
        self.target_click_state = {coord: False for coord in self.target_coords}  # Dict to track state of each target

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            if self.rect.collidepoint(pos):
                email_height = 60
                for index, email in enumerate(self.emails):
                    email_rect = pygame.Rect(self.rect.x, self.rect.y + index * email_height, self.rect.width, email_height)
                    if email_rect.collidepoint(pos):
                        self.selected_email = email
                        self.correct_clicks = []  # Reset correct clicks when a new email is selected
                        if self.selected_email.loaded_image is None:
                            self.selected_email.loaded_image = pygame.image.load(self.selected_email.image)

            if self.selected_email and self.selected_email.subject == "Urgent : informations de compte":
                image_rect = pygame.Rect(self.rect.right + 10, self.rect.y, self.selected_email.loaded_image.get_width(), self.selected_email.loaded_image.get_height())
                if image_rect.collidepoint(pos):
                    local_pos = (pos[0] - image_rect.x, pos[1] - image_rect.y)
                    for coord in self.target_coords:
                        if (local_pos[0] - coord[0]) ** 2 + (local_pos[1] - coord[1]) ** 2 <= self.click_radius ** 2:
                            if coord not in self.correct_clicks:
                                self.correct_clicks.append(coord)
                                self.target_click_state[coord] = True

    def draw(self, screen):
        email_height = 60
        for index, email in enumerate(self.emails):
            email_rect = pygame.Rect(self.rect.x, self.rect.y + index * email_height, self.rect.width, email_height)
            pygame.draw.rect(screen, (200, 200, 200), email_rect, 2)
            screen.blit(pygame.font.SysFont(None, 24).render(email.subject, True, (255, 255, 255)), (self.rect.x + 10, self.rect.y + index * email_height + 10))

        if self.selected_email:
            image = self.selected_email.loaded_image
            image = pygame.transform.scale(image, (image.get_width(), image.get_height()))
            screen.blit(image, (self.rect.right + 10, self.rect.y))

            if self.selected_email.subject == "Urgent : informations de compte":
                for coord in self.correct_clicks:
                    pygame.draw.circle(screen, (0, 255, 0), (self.rect.right + 10 + coord[0], self.rect.y + coord[1]), 10)

def level_1_email_page():
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    smallfont = pygame.font.SysFont('Corbel', 35)
    color = (255, 255, 255)
    color_light = (170, 170, 170)
    color_dark = (100, 100, 100)

    emails = [
        Email("Alice", "Réunion de suivi du projet Alpha", "", "picture/mail1.png"),
        Email("Bob", "Formation sécurité informatique", "", "picture/mail2.png"),
        Email("Charlie", "Mise à jour des politiques RH", "", "picture/mail3.png"),
        Email("David", "Prochaine sortie d'équipe", "", "picture/mail4.png"),
        Email("David", "Nouveau logiciel de gestion", "", "picture/mail5.png"),
        Email("David", "Urgent : informations de compte", "", "picture/mail6.png"),
    ]

    email_box = EmailBox(100, 100, 300, 600, emails)
    back_button = Button(10, 10, 100, 40, color_light, color_dark, smallfont.render('Back', True, color))
    indication_button = Button(10, 1030, 150, 40, color_light, color_dark, smallfont.render('Indication', True, color))
    correction_button = Button(1760, 1030, 150, 40, color_light, color_dark, smallfont.render('Correction', True, color))
    level_selection_button = Button(1660, 980, 250, 40, color_light, color_dark, smallfont.render('Retour aux niveaux', True, color))

    indication_message = smallfont.render(
        "Trouver parmi ces mails celui qui correspond à un phishing puis cliquez sur les informations qui",
        True, color
    )
    indication_message2 = smallfont.render(
        "prouvent que c'est un phishing. Une fois toutes les informations cliquées, vous avez gagné le niveau 1.",
        True, color
    )
    indication_message_rect = indication_message.get_rect(center=(screen.get_width() // 2, screen.get_height() - 60))
    indication_message_rect2 = indication_message2.get_rect(center=(screen.get_width() // 2, screen.get_height() - 20))
    indication_displayed = False
    level_complete = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if back_button.is_clicked(event):
                return
            if indication_button.is_clicked(event):
                indication_displayed = not indication_displayed
            if correction_button.is_clicked(event):
                if email_box.selected_email and email_box.selected_email.subject == "Urgent : informations de compte":
                    email_box.correct_clicks = email_box.target_coords[:]  # Mark all targets as clicked
                    level_complete = True
            if level_selection_button.is_clicked(event) and level_complete:
                level_selection()
                return

            email_box.handle_event(event)

        # Check for level completion if all targets are clicked
        if not level_complete and all(coord in email_box.correct_clicks for coord in email_box.target_coords):
            level_complete = True

        screen.fill((25, 25, 60))
        email_box.draw(screen)
        back_button.draw(screen)
        indication_button.draw(screen)
        correction_button.draw(screen)

        if level_complete:
            completion_message = smallfont.render("Vous avez gagné le niveau 1!", True, (0, 255, 0))
            screen.blit(completion_message, (screen.get_width() - 1000, 20))
            level_selection_button.draw(screen)

        if indication_displayed:
            screen.blit(indication_message, indication_message_rect.topleft)
            screen.blit(indication_message2, indication_message_rect2.topleft)

        pygame.display.update()
        
def level_selection():
    level_1_button = Button(width / 2 - 70, height / 2 - 60, 140, 40, color_light, color_dark, text_level_1)
    level_2_button = Button(width / 2 - 70, height / 2, 140, 40, color_light, color_dark, text_level_2)
    level_3_button = Button(width / 2 - 70, height / 2 + 60, 140, 40, color_light, color_dark, text_level_3)
    back_button = Button(10, 10, 100, 40, color_light, color_dark, smallfont.render('Back', True, color))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if back_button.is_clicked(event):
                return
            if level_1_button.is_clicked(event):
                level_screen(1)
            if level_2_button.is_clicked(event):
                level_screen(2)
            if level_3_button.is_clicked(event):
                level_screen(3)

        screen.fill((25, 25, 60))
        level_1_button.draw(screen)
        level_2_button.draw(screen)
        level_3_button.draw(screen)
        back_button.draw(screen)

        pygame.display.update()

def level_screen(level):
    login_box = InputBox(width // 2 - 70, height // 2 - 60, 140, 40)
    password_box = InputBox(width // 2 - 70, height // 2 - 10, 140, 40, is_password=True)
    submit_button = Button(width // 2 - 70, height // 2 + 60, 140, 40, color_light, color_dark, smallfont.render('Connect', True, color))
    cisco_button = Button(width // 2 + 80, height // 2 - 10, 220, 40, color_light, color_dark, smallfont.render('Lancer Cisco', True, color))
    web_button = Button(width // 2 + 80, height // 2 - 60, 220, 40, color_light, color_dark, smallfont.render('Lancer Web', True, color))
    back_button = Button(10, 10, 100, 40, color_light, color_dark, smallfont.render('Back', True, color))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if back_button.is_clicked(event):
                return
            login_box.handle_event(event)
            password_box.handle_event(event)
            if submit_button.is_clicked(event):
                def generate_hash(data):
                    return hashlib.sha256(data.encode()).hexdigest()

                # Lire les hash stockés depuis le fichier
                with open('Hachage/hashed_config.txt', 'r') as f:
                    stored_hashed_login_user = f.readline().strip()
                    stored_hashed_login_pass = f.readline().strip()

                # Lire les entrées de l'utilisateur
                input_login_user = login_box.get_text()
                input_login_pass = password_box.get_text()

                # Générer les hash des entrées de l'utilisateur
                hashed_input_login_user = generate_hash(input_login_user)
                hashed_input_login_pass = generate_hash(input_login_pass)

                # Comparer les hash
                if hashed_input_login_user == stored_hashed_login_user and hashed_input_login_pass == stored_hashed_login_pass:
                    level_1_email_page()
                else:
                    print("Nom d'utilisateur ou mot de passe incorrect")
            if cisco_button.is_clicked(event):
                def trouver_fichier(nom_cible):
                    repertoire_actuel = os.getcwd()  # Obtient le répertoire de travail actuel
                    for repertoire, sous_repertoires, fichiers in os.walk(repertoire_actuel):  # Parcourt récursivement les fichiers et répertoires dans le répertoire de travail actuel
                        if nom_cible in fichiers:  # Vérifie si le fichier cible est dans la liste des fichiers du répertoire actuel
                            return os.path.join(repertoire, nom_cible)  # Retourne le chemin absolu du fichier cible s'il est trouvé
                    return None  # Retourne None si le fichier cible n'est pas trouvé

                # Nom du fichier à rechercher
                nom_fichier = "ProjetCiscoFinal.pka"

                # Rechercher le fichier
                chemin_fichier = trouver_fichier(nom_fichier)

                # Vérifie si le fichier a été trouvé
                if chemin_fichier:
                    print(f"Le fichier {nom_fichier} a été trouvé à l'emplacement : {chemin_fichier}")
                    # Ouvrir le fichier avec l'application par défaut
                    os.startfile(chemin_fichier)
                else:
                    print(f"Le fichier {nom_fichier} n'a pas été trouvé dans le répertoire actuel ou ses sous-répertoires.")

            if web_button.is_clicked(event):
                print("La page internet va se lancer")

        screen.fill((25, 25, 60))
        login_box.draw(screen)
        password_box.draw(screen)
        submit_button.draw(screen)
        cisco_button.draw(screen)
        web_button.draw(screen)
        back_button.draw(screen)

        pygame.display.update()

# Start the main menu
main_menu()
