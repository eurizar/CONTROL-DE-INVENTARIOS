"""
Módulo para generar PDFs de documentos del sistema.
Incluye generación de facturas, recibos y reportes.
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from datetime import datetime
import os


class PDFGenerator:
    """Generador de PDFs para el sistema de inventarios."""
    
    def __init__(self, empresa_nombre="Mi Empresa", empresa_nit="", empresa_direccion="", empresa_telefono="", empresa_email="", logo_path=None):
        """
        Inicializa el generador de PDFs con información de la empresa.
        
        Args:
            empresa_nombre: Nombre de la empresa
            empresa_nit: NIT de la empresa
            empresa_direccion: Dirección de la empresa
            empresa_telefono: Teléfono de la empresa
            empresa_email: Email de la empresa (opcional)
            logo_path: Ruta al archivo de logo (opcional)
        """
        self.empresa_nombre = empresa_nombre
        self.empresa_nit = empresa_nit
        self.empresa_direccion = empresa_direccion
        self.empresa_telefono = empresa_telefono
        self.empresa_email = empresa_email
        self.logo_path = logo_path
        self.styles = getSampleStyleSheet()
        
        # Crear estilos personalizados
        self.styles.add(ParagraphStyle(
            name='CenterBold',
            parent=self.styles['Heading1'],
            alignment=TA_CENTER,
            fontSize=16,
            textColor=colors.HexColor('#2c3e50')
        ))
        
        self.styles.add(ParagraphStyle(
            name='RightAlign',
            parent=self.styles['Normal'],
            alignment=TA_RIGHT
        ))
    
    def generar_factura_venta(self, venta_data, archivo_salida):
        """
        Genera un PDF de factura para una venta.
        
        Args:
            venta_data: Diccionario con información de la venta:
                - referencia_no: Número de referencia
                - fecha: Fecha de la venta
                - estado: Estado de la venta
                - cliente_nombre: Nombre del cliente
                - cliente_nit: NIT del cliente
                - detalles: Lista de productos vendidos
                - total: Total de la venta
                - monto_pagado: Monto pagado (opcional)
                - cambio: Cambio devuelto (opcional)
            archivo_salida: Ruta completa donde guardar el PDF
        
        Returns:
            Tuple[bool, str]: (éxito, mensaje)
        """
        try:
            # Crear documento
            doc = SimpleDocTemplate(
                archivo_salida,
                pagesize=letter,
                rightMargin=0.5*inch,
                leftMargin=0.5*inch,
                topMargin=0.5*inch,
                bottomMargin=0.5*inch
            )
            
            # Lista de elementos del documento
            elementos = []
            
            # ===== ENCABEZADO CON LOGO =====
            encabezado_data = []
            
            # Intentar cargar logo si existe
            logo = None
            if self.logo_path and os.path.exists(self.logo_path):
                try:
                    logo = Image(self.logo_path, width=1.2*inch, height=1.2*inch)  # Reducido de 1.5 a 1.2
                except Exception as e:
                    print(f"No se pudo cargar el logo: {e}")
            
            # Crear tabla de encabezado con logo y datos de empresa
            if logo:
                # Estilo personalizado para el membrete con fuente más grande
                estilo_membrete = ParagraphStyle(
                    name='Membrete',
                    parent=self.styles['Normal'],
                    fontSize=11,  # Aumentado de 10 a 11
                    leading=13,   # Espacio entre líneas reducido de 14 a 13
                )
                
                estilo_membrete_titulo = ParagraphStyle(
                    name='MembreteTitulo',
                    parent=self.styles['Normal'],
                    fontSize=13,  # Aumentado para el título
                    leading=15,   # Espacio entre líneas reducido de 16 a 15
                    fontName='Helvetica-Bold'
                )
                
                # Info de la empresa como texto con fuente más grande
                empresa_info = [
                    [Paragraph(f"<b>{self.empresa_nombre.upper()}</b>", estilo_membrete_titulo)],
                ]
                if self.empresa_nit:
                    empresa_info.append([Paragraph(f"NIT: {self.empresa_nit}", estilo_membrete)])
                if self.empresa_direccion:
                    empresa_info.append([Paragraph(self.empresa_direccion, estilo_membrete)])
                if self.empresa_telefono:
                    empresa_info.append([Paragraph(f"Tel: {self.empresa_telefono}", estilo_membrete)])
                if self.empresa_email:
                    empresa_info.append([Paragraph(f"Email: {self.empresa_email}", estilo_membrete)])
                
                empresa_table = Table(empresa_info, colWidths=[4.5*inch])
                empresa_table.setStyle(TableStyle([
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 0),  # Sin padding izquierdo
                    ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                    ('TOPPADDING', (0, 0), (-1, -1), 0),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
                ]))
                
                # Tabla de encabezado con membrete a la izquierda y logo a la derecha
                encabezado_table = Table([[empresa_table, logo]], colWidths=[4.8*inch, 1.8*inch])
                encabezado_table.setStyle(TableStyle([
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                    ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 0),  # Sin padding izquierdo
                    ('RIGHTPADDING', (0, 0), (-1, -1), 0),  # Sin padding derecho
                    ('LEFTPADDING', (1, 0), (1, 0), 10),  # Reducido de 20 a 10
                    ('TOPPADDING', (1, 0), (1, 0), 0),   # Alineado con el membrete (cambiado de -5 a 0)
                ]))
                elementos.append(encabezado_table)
            else:
                # Sin logo, solo texto centrado
                titulo = Paragraph(f"<b>{self.empresa_nombre.upper()}</b>", self.styles['CenterBold'])
                elementos.append(titulo)
                elementos.append(Spacer(1, 0.1*inch))
                
                if self.empresa_nit:
                    nit_empresa = Paragraph(f"NIT: {self.empresa_nit}", self.styles['Normal'])
                    nit_empresa.alignment = TA_CENTER
                    elementos.append(nit_empresa)
                
                if self.empresa_direccion:
                    direccion = Paragraph(self.empresa_direccion, self.styles['Normal'])
                    direccion.alignment = TA_CENTER
                    elementos.append(direccion)
                
                if self.empresa_telefono:
                    telefono = Paragraph(f"Tel: {self.empresa_telefono}", self.styles['Normal'])
                    telefono.alignment = TA_CENTER
                    elementos.append(telefono)
                
                if self.empresa_email:
                    email = Paragraph(f"Email: {self.empresa_email}", self.styles['Normal'])
                    email.alignment = TA_CENTER
                    elementos.append(email)
            
            elementos.append(Spacer(1, 0.3*inch))
            
            # ===== TÍTULO DEL DOCUMENTO =====
            tipo_doc = "RECIBO" if venta_data.get('estado') == 'Emitido' else "RECIBO ANULADO"
            estilo_titulo = ParagraphStyle(
                name='TituloDoc',
                parent=self.styles['Heading2'],
                alignment=TA_CENTER,
                fontSize=14,
                textColor=colors.red if venta_data.get('estado') == 'Anulado' else colors.HexColor('#27ae60')
            )
            titulo_doc = Paragraph(tipo_doc, estilo_titulo)
            elementos.append(titulo_doc)
            elementos.append(Spacer(1, 0.2*inch))
            
            # ===== INFORMACIÓN DE LA VENTA =====
            info_data = [
                ['Referencia:', venta_data['referencia_no'], 'Fecha:', venta_data['fecha']],
                ['Cliente:', venta_data['cliente_nombre'], 'NIT/DPI:', venta_data.get('cliente_nit', '')],
                ['Dirección:', venta_data.get('cliente_direccion', 'N/A'), 'Teléfono:', venta_data.get('cliente_telefono', 'N/A')],
                ['Estado:', venta_data.get('estado', 'Emitido'), '', '']
            ]
            
            info_table = Table(info_data, colWidths=[1.2*inch, 2.5*inch, 1*inch, 2*inch])
            info_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2c3e50')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),  # Reducido de 8 a 4
                ('TOPPADDING', (0, 0), (-1, -1), 2),     # Reducido el padding superior
                ('LEFTPADDING', (0, 0), (-1, -1), 0),    # Sin padding izquierdo
                ('RIGHTPADDING', (0, 0), (-1, -1), 0),   # Sin padding derecho
            ]))
            
            elementos.append(info_table)
            elementos.append(Spacer(1, 0.3*inch))
            
            # ===== TABLA DE PRODUCTOS =====
            # Encabezados
            productos_data = [['Producto', 'Cant.', 'P. Orig.', 'Desc %', 'P. Final', 'Subtotal']]
            
            # Datos de productos
            for detalle in venta_data['detalles']:
                # Obtener información de descuento si existe
                precio_original = detalle.get('precio_original', detalle['precio_unitario'])
                precio_final = detalle['precio_unitario']
                
                # Calcular descuento
                if precio_final < precio_original:
                    descuento_pct = ((precio_original - precio_final) / precio_original) * 100
                    descuento_str = f"{descuento_pct:.1f}%"
                else:
                    descuento_str = "-"
                
                productos_data.append([
                    detalle['producto_nombre'][:30],
                    str(detalle['cantidad']),
                    f"Q {precio_original:,.2f}",
                    descuento_str,
                    f"Q {precio_final:,.2f}",
                    f"Q {detalle['subtotal']:,.2f}"
                ])
            
            # Crear tabla
            productos_table = Table(productos_data, colWidths=[2.5*inch, 0.6*inch, 1*inch, 0.8*inch, 1*inch, 1*inch])
            productos_table.setStyle(TableStyle([
                # Encabezado
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('ALIGN', (1, 0), (-1, 0), 'CENTER'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                ('LEFTPADDING', (0, 0), (0, 0), 0),  # Sin padding izquierdo en primera columna
                
                # Datos
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
                ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),
                ('VALIGN', (0, 1), (-1, -1), 'MIDDLE'),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
                ('TOPPADDING', (0, 1), (-1, -1), 6),
                ('LEFTPADDING', (0, 1), (0, -1), 0),  # Sin padding izquierdo en primera columna
                
                # Líneas
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('LINEBELOW', (0, 0), (-1, 0), 2, colors.HexColor('#34495e')),
            ]))
            
            elementos.append(productos_table)
            elementos.append(Spacer(1, 0.3*inch))
            
            # ===== TOTALES =====
            totales_data = []
            
            # Total
            totales_data.append(['', '', '', '', 'TOTAL:', f"Q {venta_data['total']:,.2f}"])
            
            # Monto pagado y cambio (si están disponibles)
            if venta_data.get('monto_pagado') and venta_data['monto_pagado'] > 0:
                totales_data.append(['', '', '', '', 'Pagado:', f"Q {venta_data['monto_pagado']:,.2f}"])
                totales_data.append(['', '', '', '', 'Cambio:', f"Q {venta_data.get('cambio', 0):,.2f}"])
            
            totales_table = Table(totales_data, colWidths=[2.5*inch, 0.6*inch, 1*inch, 0.8*inch, 1*inch, 1*inch])
            totales_table.setStyle(TableStyle([
                ('FONTNAME', (4, 0), (4, -1), 'Helvetica-Bold'),
                ('FONTNAME', (5, 0), (5, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (4, 0), (5, 0), 12),
                ('FONTSIZE', (4, 1), (5, -1), 10),
                ('ALIGN', (4, 0), (5, -1), 'RIGHT'),
                ('TEXTCOLOR', (4, 0), (5, 0), colors.HexColor('#27ae60')),
                ('LINEABOVE', (4, 0), (5, 0), 2, colors.HexColor('#27ae60')),
                ('BOTTOMPADDING', (4, 0), (5, -1), 6),
            ]))
            
            elementos.append(totales_table)
            elementos.append(Spacer(1, 0.5*inch))
            
            # ===== PIE DE PÁGINA =====
            fecha_generacion = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            pie = Paragraph(f"<i>Documento generado el {fecha_generacion}</i>", self.styles['Normal'])
            pie.alignment = TA_CENTER
            elementos.append(pie)
            
            if venta_data.get('estado') == 'Anulado':
                anulado_text = Paragraph(
                    "<b>*** DOCUMENTO ANULADO - SIN VALIDEZ ***</b>",
                    ParagraphStyle(
                        name='Anulado',
                        parent=self.styles['Normal'],
                        alignment=TA_CENTER,
                        textColor=colors.red,
                        fontSize=12
                    )
                )
                elementos.append(Spacer(1, 0.2*inch))
                elementos.append(anulado_text)
            
            # Construir PDF
            doc.build(elementos)
            
            return True, f"PDF generado exitosamente: {archivo_salida}"
            
        except Exception as e:
            return False, f"Error al generar PDF: {str(e)}"


def generar_pdf_venta(venta_data, directorio_salida=None):
    """
    Función de utilidad para generar PDF de una venta.
    
    Args:
        venta_data: Datos de la venta
        directorio_salida: Directorio donde guardar el PDF (None = Documentos del usuario)
    
    Returns:
        Tuple[bool, str]: (éxito, ruta del archivo o mensaje de error)
    """
    try:
        # Determinar directorio de salida
        if directorio_salida is None:
            from pathlib import Path
            directorio_salida = str(Path.home() / "Documents" / "Recibos")
        
        # Crear directorio si no existe
        os.makedirs(directorio_salida, exist_ok=True)
        
        # Nombre del archivo
        nombre_archivo = f"Recibo_{venta_data['referencia_no']}.pdf"
        ruta_completa = os.path.join(directorio_salida, nombre_archivo)
        
        # Generar PDF
        generador = PDFGenerator(
            empresa_nombre="Sistema de Control de Inventarios",
            empresa_nit="",
            empresa_direccion="",
            empresa_telefono=""
        )
        
        exito, mensaje = generador.generar_factura_venta(venta_data, ruta_completa)
        
        if exito:
            return True, ruta_completa
        else:
            return False, mensaje
            
    except Exception as e:
        return False, f"Error al generar PDF: {str(e)}"
