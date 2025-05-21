from PIL import Image, ImageDraw, ImageFont
import os

class CertificateGenerator:
    def __init__(self):
        # Rutas base
        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        self.assets_dir = os.path.join(self.base_dir, 'assets')
        self.certificates_dir = os.path.join(self.base_dir, 'certificates')
        
        # Crear directorios necesarios
        os.makedirs(self.assets_dir, exist_ok=True)
        os.makedirs(self.certificates_dir, exist_ok=True)
        
        # Rutas de recursos
        self.template_path = os.path.join(self.assets_dir, 'certificate_template.png')
        self.font_path = os.path.join(self.assets_dir, 'Montserrat-Regular.ttf')
        self.font_bold_path = os.path.join(self.assets_dir, 'Montserrat-Bold.ttf')
    
    def generate(self, data):
        """
        Genera un certificado visual
        
        Args:
            data (dict): Diccionario con la información del certificado
                - participante (str): Nombre del participante
                - cedula (str): Número de cédula
                - proyecto (str): Nombre del proyecto
                - fecha (str): Fecha del proyecto
                - firmantes (list): Lista de firmantes
        
        Returns:
            str: Ruta del certificado generado
        """
        # Abrir la plantilla
        img = Image.open(self.template_path)
        draw = ImageDraw.Draw(img)
        
        # Configurar fuentes
        font_regular = ImageFont.truetype(self.font_path, 36)
        font_bold = ImageFont.truetype(self.font_bold_path, 48)
        font_small = ImageFont.truetype(self.font_path, 24)
        
        # Posiciones
        width, height = img.size
        center_x = width / 2
        
        # Nombre del participante
        draw.text(
            (center_x, 320),
            data['participante'],
            font=font_bold,
            fill='rgb(0, 0, 139)',
            anchor="mm"
        )
        
        # Cédula
        draw.text(
            (center_x, 380),
            f"C.I. {data['cedula']}",
            font=font_regular,
            fill='black',
            anchor="mm"
        )
        
        # Texto del proyecto
        proyecto_text = f'Por haber participado en la 4ta Expoferia de la Escuela de Ingeniería con el proyecto "{data["proyecto"]}", realizado el {data["fecha"]}.'
        
        # Dividir el texto en líneas
        words = proyecto_text.split()
        lines = []
        current_line = []
        
        for word in words:
            current_line.append(word)
            text = ' '.join(current_line)
            if draw.textlength(text, font=font_small) > width - 200:
                current_line.pop()
                lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        # Dibujar las líneas de texto
        y_position = 440
        for line in lines:
            draw.text(
                (center_x, y_position),
                line,
                font=font_small,
                fill='black',
                anchor="mm"
            )
            y_position += 30
        
        # Guardar el certificado
        output_path = os.path.join(
            self.certificates_dir,
            f'certificado_{data["cedula"]}.png'
        )
        
        # Guardar imagen
        img.save(output_path)
        return output_path