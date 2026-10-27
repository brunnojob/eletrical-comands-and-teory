from . import learning, learning_pt


UI_PT = {
    'Simulator': 'Simulador',
    'Theory': 'Teoria',
    'Motor Sizing': 'Dimensionamento de motores',
    'Multimeter': 'Multímetro',
    'Projects': 'Projetos',
    'How to Build': 'Planejamento e montagem',
    'Training': 'Treinamento',
    'Electrical Controls': 'Comandos Elétricos',
    'Electrical Controls Lab · Brunno Dev': 'Laboratório de Comandos Elétricos · Brunno Dev',
    'BRUNNO DEV / PYTHON LAB': 'BRUNNO DEV / LABORATÓRIO PYTHON',
    '● Local workspace': '● Área de trabalho local',
    'Sponsor ↗': 'Apoiar ↗',
    'WORKSPACE': 'ÁREA DE TRABALHO',
    'Tools': 'Ferramentas',
    'No account needed': 'Sem necessidade de conta',
    'Projects stay in your browser.': 'Os projetos ficam no seu navegador.',
    'Export a backup to keep a copy.': 'Exporte um backup para guardar uma cópia.',
    'Loading the Python workspace…': 'Carregando a área de trabalho Python…',
    'If this takes too long, check access to cdn.jsdelivr.net and reload.': 'Se demorar, verifique o acesso a cdn.jsdelivr.net e recarregue.',
    'Enable browser scripting to run the Python interpreter.': 'Ative os scripts do navegador para executar o interpretador Python.',
    'MIT License': 'Licença MIT',
    'Learning simulation · no connection to physical equipment': 'Simulação didática · sem conexão com equipamentos físicos',
    'Language': 'Idioma',
    'English': 'Inglês',
    'Portuguese (Brazil)': 'Português (Brasil)',
    'Theme': 'Tema',
    'Dark': 'Escuro',
    'Light': 'Claro',
    'Circuit': 'Circuito',
    'Line voltage': 'Tensão de linha',
    'Fit': 'Ajustar',
    'Reset': 'Reiniciar',
    'Every scan advances simulated time by 1 second. Coil feedback is visible on the next scan. The diagram is conceptual.': 'Cada ciclo avança o tempo simulado em 1 segundo. A realimentação das bobinas fica disponível no ciclo seguinte. O diagrama é conceitual.',
    'Input signals': 'Sinais de entrada',
    'Outputs': 'Saídas',
    'Events & alarms': 'Eventos e alarmes',
    'Edit NO / NC contacts, AND / OR branches, TON timers, coils and interlock groups. Loading an invalid definition preserves the current circuit.': 'Edite contatos NA / NF, ramificações E / OU, temporizadores TON, bobinas e grupos de intertravamento. Uma definição inválida mantém o circuito atual.',
    'Circuit JSON': 'JSON do circuito',
    'Load circuit': 'Carregar circuito',
    'Structured Text ↓': 'Texto Estruturado ↓',
    'Search topics': 'Pesquisar assuntos',
    'Motor data': 'Dados do motor',
    'Poles': 'Polos',
    'Frequency (Hz)': 'Frequência (Hz)',
    'Estimated slip (0–1)': 'Escorregamento estimado (0–1)',
    'Calculation results': 'Resultados do cálculo',
    'Calculate': 'Calcular',
    'Power conversion': 'Conversão de potência',
    'Value': 'Valor',
    'From': 'De',
    'Virtual multimeter': 'Multímetro virtual',
    'Simulated readings only. AC uses a balanced three-phase supply with an ideal N–PE bond; DC uses L1 = +24 V and all other points = 0 V.': 'Somente leituras simuladas. Em CA, a alimentação trifásica é equilibrada, com ligação N–PE ideal; em CC, L1 = +24 V e os demais pontos = 0 V.',
    'Measurement': 'Medição',
    'AC voltage': 'Tensão CA',
    'DC voltage': 'Tensão CC',
    'AC current': 'Corrente CA',
    'Continuity': 'Continuidade',
    'Red probe': 'Ponta de prova vermelha',
    'Black probe': 'Ponta de prova preta',
    'Reading a motor nameplate': 'Leitura da placa de identificação do motor',
    'Import JSON': 'Importar JSON',
    'Project name': 'Nome do projeto',
    'Motor power (kW)': 'Potência do motor (kW)',
    'Voltage (V)': 'Tensão (V)',
    'Description': 'Descrição',
    'Status': 'Situação',
    'Save project': 'Salvar projeto',
    'Remove project': 'Remover projeto',
    'Cancel': 'Cancelar',
    'Export backup ↓': 'Exportar backup ↓',
    'Saved projects': 'Projetos salvos',
    'Ready-to-use templates': 'Modelos prontos para usar',
    "Storage is specific to this browser and site address. Netlify data does not automatically move to GitHub Pages. JSON imports also accept the original site's project records.": 'O armazenamento é específico deste navegador e endereço do site. Dados do Netlify não são transferidos automaticamente para o GitHub Pages. A importação JSON também aceita os registros de projetos do site anterior.',
    'Project plan & materials': 'Planejamento e materiais do projeto',
    'Planning aid for study. Final wiring, ratings and protection settings require a reviewed design and manufacturer documentation.': 'Auxílio ao planejamento para estudo. A ligação final, as capacidades nominais e os ajustes de proteção exigem projeto revisado e documentação do fabricante.',
    'Materials CSV ↓': 'Materiais CSV ↓',
    'Print / PDF': 'Imprimir / PDF',
    'Build & review checklist': 'Lista de montagem e revisão',
    'Retry': 'Tentar novamente',
    'Practice in the simulator': 'Pratique no simulador',
    'Explore electrical control sequences and test the logic, one scan at a time.': 'Explore sequências de comandos elétricos e teste a lógica, um ciclo de cada vez.',
    'The principles behind motors, protection and electrical control.': 'Os princípios dos motores, da proteção e dos comandos elétricos.',
    'Estimate motor current, speed and component references.': 'Estime a corrente e a velocidade do motor e consulte referências de componentes.',
    'Explore voltage, current and continuity in a virtual circuit.': 'Explore tensão, corrente e continuidade em um circuito virtual.',
    'Create, organize and back up projects in your browser.': 'Crie, organize e exporte backups dos projetos no navegador.',
    'Plan materials and track your design review.': 'Planeje materiais e acompanhe a revisão do projeto.',
    'Test your knowledge and practice with circuit challenges.': 'Teste seus conhecimentos e pratique com desafios de circuitos.',
    'Scan time': 'Tempo simulado',
    'Active outputs': 'Saídas ativas',
    'Sequence': 'Sequência',
    'scans': 'ciclos',
    'Single-line & control diagram': 'Diagrama unifilar e de comando',
    '← Previous': '← Anterior',
    'Pause': 'Pausar',
    'Auto play': 'Reproduzir automaticamente',
    'Next scan →': 'Próximo ciclo →',
    'Next step →': 'Próxima etapa →',
    'Frequency reference (Hz)': 'Referência de frequência (Hz)',
    'Acknowledge alarms': 'Reconhecer alarmes',
    'No transitions yet. Start the sequence or toggle an input.': 'Nenhuma transição ainda. Inicie a sequência ou altere uma entrada.',
    'Circuit editor & PLC export': 'Editor de circuitos e exportação para CLP',
    'Mechanical output power (kW)': 'Potência mecânica de saída (kW)',
    'Line voltage (V)': 'Tensão de linha (V)',
    'Power factor (0–1)': 'Fator de potência (0–1)',
    'Efficiency (0–1)': 'Rendimento (0–1)',
    'The model assumes an ideal balanced supply. Actual readings depend on the real circuit and equipment.': 'O modelo considera uma alimentação ideal e equilibrada. As leituras reais dependem do circuito e dos equipamentos.',
    'Import files must be smaller than 2 MB.': 'Os arquivos de importação devem ter menos de 2 MB.',
    'Edit project': 'Editar projeto',
    'New project': 'Novo projeto',
    'draft': 'Rascunho',
    'review': 'Em revisão',
    'ready': 'Pronto',
    'The workspace can hold at most 500 projects.': 'A área de trabalho comporta no máximo 500 projetos.',
    'Open': 'Abrir',
    'Edit': 'Editar',
    'Copy': 'Copiar',
    'Remove': 'Remover',
    'No saved projects yet. Create one above or use a template below.': 'Nenhum projeto salvo ainda. Crie um acima ou use um dos modelos abaixo.',
    'Use template': 'Usar modelo',
    'Selection reference': 'Referência para seleção',
    'Parameter': 'Parâmetro',
    'Estimate': 'Estimativa',
    'Item': 'Item',
    'Quantity': 'Quantidade',
    'Marking': 'Marcação',
    'Meaning': 'Significado',
    'Next →': 'Próxima →',
    'Start the motor, release START, then test STOP.': 'Ligue o motor, solte o comando de partida e teste o comando de parada.',
    'Request both directions and inspect the conflict event.': 'Solicite os dois sentidos e examine o evento de conflito.',
    'Advance scans and observe star release before delta starts.': 'Avance os ciclos e observe a abertura da estrela antes da entrada do triângulo.',
    'Remove PHASE B while running. Restore it and test restart.': 'Interrompa a fase B durante o funcionamento. Restabeleça-a e teste a nova partida.',
    'Follow red, green and yellow without overlapping outputs.': 'Acompanhe vermelho, verde e amarelo sem sobreposição de saídas.',
    'Compare enable, run and fault signals.': 'Compare os sinais de habilitação, funcionamento e falha.',
    'Open simulator': 'Abrir simulador',
    'ELECTRICAL CONTROLS LAB': 'LABORATÓRIO DE COMANDOS ELÉTRICOS',
    'PYTHON / BROWSER': 'PYTHON / NAVEGADOR',
    'Browser storage is unavailable. Export a backup before closing this page.': 'O armazenamento do navegador está indisponível. Exporte um backup antes de fechar esta página.',
    'Browser storage is unavailable or full. Export a backup before closing this page.': 'O armazenamento do navegador está indisponível ou cheio. Exporte um backup antes de fechar esta página.',
    'Saved data could not be read. The original storage was left untouched; import a valid backup to recover it.': 'Não foi possível ler os dados salvos. O armazenamento original foi preservado; importe um backup válido para recuperá-los.',
    'Phase failure': 'Falta de fase',
    'Manual scan': 'Ciclo manual',
    'Custom circuit: toggle inputs and advance scans.': 'Circuito personalizado: altere as entradas e avance os ciclos.',
    'ON': 'LIGADO',
    'OFF': 'DESLIGADO',
    'Drive stopped': 'Inversor parado',
    'Custom circuit loaded.': 'Circuito personalizado carregado.',
    'I = P / (√3 × V × power factor × efficiency). Starting current uses an assumed multiplier. Cable and protective-device values are study examples, not installation selections; check installation method, derating, voltage drop, fault level, starting duty and manufacturer coordination.': 'I = P / (√3 × V × fator de potência × rendimento). A corrente de partida usa um multiplicador estimado. Os valores de cabos e dispositivos de proteção são exemplos de estudo, não seleções para instalação; verifique método de instalação, fatores de correção, queda de tensão, nível de curto-circuito, regime de partida e coordenação do fabricante.',
    'Results JSON ↓': 'Resultados JSON ↓',
    'Modeled clamp reading on the selected red-probe conductor for a 7.5 kW load. The black probe is unused in clamp mode. No live measurement is performed.': 'Leitura simulada de alicate amperímetro no condutor da ponta vermelha para uma carga de 7,5 kW. A ponta preta não é usada neste modo. Nenhuma medição real é realizada.',
    'Ω / continuity': 'Ω / continuidade',
    'A separate de-energized topology model is used here. It assumes an N–PE bond and no path between different phase points. This does not describe or verify any physical installation.': 'Aqui é usado um modelo separado de topologia desenergizada, com ligação N–PE e sem caminho entre fases diferentes. Ele não descreve nem verifica uma instalação física.',
    'Mechanical shaft output power': 'Potência mecânica de saída no eixo',
    'Rated voltage for each winding connection': 'Tensão nominal para cada ligação dos enrolamentos',
    'Rated current for the specified connection and duty': 'Corrente nominal para a ligação e o regime especificados',
    'Rated frequency and shaft speed': 'Frequência nominal e velocidade do eixo',
    'Power factor and efficiency': 'Fator de potência e rendimento',
    'IP / duty / insulation': 'IP / regime / isolação',
    'Environmental protection, operating duty and insulation classification': 'Grau de proteção, regime de funcionamento e classe de isolação',
    'The selected file could not be read.': 'Não foi possível ler o arquivo selecionado.',
    'No description.': 'Sem descrição.',
    'Current simulator circuit': 'Circuito atual do simulador',
    'Enter a nonnegative finite power.': 'Informe uma potência finita maior ou igual a zero.',
    'Project saved in this browser.': 'Projeto salvo neste navegador.',
    'Use a frequency between 0 and 120 Hz.': 'Use uma frequência entre 0 e 120 Hz.',
    'Rated current': 'Corrente nominal',
    'DOL starting current (7×)': 'Corrente de partida direta (7×)',
    'Synchronous speed': 'Velocidade síncrona',
    'Speed with estimated slip': 'Velocidade com escorregamento estimado',
    'Illustrative copper section': 'Seção ilustrativa de cobre',
    'Illustrative breaker (1.25×)': 'Disjuntor ilustrativo (1,25×)',
    'Overload current reference': 'Referência de corrente de sobrecarga',
    'Illustrative fuse (1.6×)': 'Fusível ilustrativo (1,6×)',
    'Export and remove projects before adding more than 500.': 'Exporte e remova projetos antes de adicionar mais de 500.',
    'Outside table': 'Fora da tabela',
    'Correct. ': 'Correto. ',
    'Try again. ': 'Tente novamente. ',
    'Alarms acknowledged': 'Alarmes reconhecidos',
    'POWER OVERVIEW · SIMPLIFIED': 'VISÃO DE POTÊNCIA · SIMPLIFICADA',
    'CONTROL LOGIC · PREVIOUS-SCAN FEEDBACK': 'LÓGICA DE COMANDO · REALIMENTAÇÃO DO CICLO ANTERIOR',
    'Electrical control schematic': 'Esquema de comando elétrico',
    '3~ SUPPLY': 'ALIMENTAÇÃO 3~',
    'ISOLATOR': 'SECCIONADORA',
    'PROTECTION': 'PROTEÇÃO',
    'CONTACTOR / DRIVE': 'CONTATOR / INVERSOR',
    'MOTOR / LOAD': 'MOTOR / CARGA',
    'SAFE': 'PERMISSIVO',
    'START': 'PARTIDA',
    'STOP': 'PARADA',
    'START FWD': 'PARTIDA DIRETA',
    'START REV': 'PARTIDA REVERSA',
    'FORWARD': 'DIRETO',
    'REVERSE': 'REVERSO',
    'MAIN': 'PRINCIPAL',
    'STAR': 'ESTRELA',
    'DELTA': 'TRIÂNGULO',
    'STAR DONE': 'TEMPO ESTRELA CONCLUÍDO',
    'DELTA READY': 'TRIÂNGULO LIBERADO',
    'STAR TIME': 'TEMPO ESTRELA',
    'DEAD TIME': 'TEMPO MORTO',
    'RED': 'VERMELHO',
    'GREEN': 'VERDE',
    'YELLOW': 'AMARELO',
    'RED REQUEST': 'COMANDO VERMELHO',
    'GREEN REQUEST': 'COMANDO VERDE',
    'YELLOW REQUEST': 'COMANDO AMARELO',
    'PHASE A': 'FASE A',
    'PHASE B': 'FASE B',
    'PHASE C': 'FASE C',
    'ENABLE': 'HABILITAÇÃO',
    'RUN': 'FUNCIONAMENTO',
    'FAULT': 'FALHA',
    'DRIVE RUN': 'INVERSOR LIGADO',
    'Direct-On-Line': 'Partida direta',
    'Reversal': 'Reversão',
    'Star-Delta': 'Estrela-triângulo',
    'Traffic Light': 'Semáforo',
    'Phase Failure': 'Falta de fase',
    'VFD': 'Inversor de frequência',
    'Enter finite numeric values.': 'Informe valores numéricos finitos.',
    'Check power, voltage, power factor, efficiency, poles, frequency and slip.': 'Verifique potência, tensão, fator de potência, rendimento, polos, frequência e escorregamento.',
    'Isolator': 'Seccionadora',
    'Rated for the supply and load': 'Compatível com a alimentação e a carga',
    'Short-circuit protection': 'Proteção contra curto-circuito',
    'Coordinate with the selected equipment': 'Coordenar com os equipamentos selecionados',
    'Contactor': 'Contator',
    'Overload protection': 'Proteção contra sobrecarga',
    'Start / stop controls': 'Comandos de partida e parada',
    'Control voltage and enclosure rating': 'Tensão de comando e grau de proteção do invólucro',
    'Terminals, conductors and enclosure': 'Bornes, condutores e invólucro',
    'Select for the installation conditions': 'Selecionar conforme as condições de instalação',
    'Mechanical interlock': 'Intertravamento mecânico',
    'Compatible reversing contactors': 'Contatores de reversão compatíveis',
    'Phase monitoring relay': 'Relé de monitoramento de fases',
    'Voltage and phase sequence compatible': 'Compatível com a tensão e a sequência de fases',
    'Variable frequency drive': 'Inversor de frequência',
    'Match motor, supply, duty and environment': 'Compatível com motor, alimentação, regime e ambiente',
    'Star-delta timer': 'Temporizador estrela-triângulo',
    'Open transition': 'Transição aberta',
    'Star and delta contactors': 'Contatores estrela e triângulo',
    'Untitled project': 'Projeto sem título',
    'Invalid project record.': 'Registro de projeto inválido.',
    'Unknown circuit type.': 'Tipo de circuito desconhecido.',
    'Project name must contain 1–120 characters.': 'O nome do projeto deve ter de 1 a 120 caracteres.',
    'Power and voltage must be positive finite numbers.': 'Potência e tensão devem ser números finitos e positivos.',
    'Invalid project description.': 'Descrição de projeto inválida.',
    'Import a project list or an exported backup with at most 500 projects.': 'Importe uma lista ou um backup exportado com no máximo 500 projetos.',
    'invalid_coils': 'A definição de bobinas é inválida; use uma lista com até 128 bobinas.',
    'invalid_coil_id': 'O identificador da bobina é inválido ou está repetido.',
    'invalid_interlocks': 'A lista de intertravamentos é inválida.',
    'invalid_interlock': 'O grupo de intertravamento é inválido.',
    'invalid_logic': 'A lógica é inválida ou excede a profundidade permitida.',
    'invalid_contact': 'O contato é inválido; verifique o sinal e o modo NO / NC.',
    'invalid_children': 'A ramificação precisa ter de 1 a 128 elementos.',
    'invalid_timer_id': 'O identificador do temporizador é inválido ou está repetido.',
    'invalid_timer_delay': 'O atraso do temporizador deve estar entre 0 e 3600000 ms.',
    'unknown_logic_type': 'Tipo de lógica desconhecido.',
    'invalid_scan_time': 'O tempo do ciclo é inválido ou não avança.',
    'invalid_inputs': 'As entradas precisam conter valores booleanos.',
    'coil_input_override': 'Uma entrada não pode sobrescrever uma saída de bobina.',
    'invalid_probe': 'Ponta de prova inválida.',
    'invalid_block_name': 'Nome do bloco de CLP inválido.',
    'integer_timer_delay_required': 'O atraso do temporizador deve ser um número inteiro de milissegundos.',
    'Start, seal-in and stop a three-phase motor.': 'Partida, selo e parada de um motor trifásico.',
    'Forward and reverse contactors with electrical interlocks.': 'Contatores de sentido direto e reverso com intertravamentos elétricos.',
    'Star acceleration, an open transition and delta operation.': 'Aceleração em estrela, transição aberta e operação em triângulo.',
    'A sequenced signal with mutually exclusive outputs.': 'Sinalização sequencial com saídas mutuamente exclusivas.',
    'Loss of any phase removes the motor permissive.': 'A falta de qualquer fase retira o permissivo do motor.',
    'Enable, run and fault permissives with a frequency reference.': 'Permissivos de habilitação, funcionamento e falha com referência de frequência.',
    'Ready': 'Pronto',
    'Press START': 'Acione a partida',
    'Release START: the auxiliary contact holds': 'Solte a partida: o contato auxiliar mantém o selo',
    'Press STOP': 'Acione a parada',
    'Release STOP': 'Solte a parada',
    'Forward start': 'Partida no sentido direto',
    'Forward held': 'Sentido direto mantido pelo selo',
    'Stop before reversing': 'Pare antes de inverter o sentido',
    'Reverse start': 'Partida no sentido reverso',
    'Reverse held': 'Sentido reverso mantido pelo selo',
    'Stop': 'Parada',
    'Start main contactor': 'Acione o contator principal',
    'Star acceleration': 'Aceleração em estrela',
    'Star timer reaches its preset': 'O temporizador de estrela alcança o tempo ajustado',
    'Star opens': 'O contator estrela abre',
    'Delta operation': 'Operação em triângulo',
    'Red: stop': 'Vermelho: pare',
    'Green: go': 'Verde: siga',
    'Yellow: prepare to stop': 'Amarelo: prepare-se para parar',
    'All phases healthy': 'Todas as fases presentes',
    'Start motor': 'Dê partida no motor',
    'Running': 'Em funcionamento',
    'Phase B lost: motor trips': 'Fase B interrompida: o motor desliga',
    'Phase B restored: restart required': 'Fase B restabelecida: nova partida necessária',
    'Restart': 'Nova partida',
    'Drive disabled': 'Inversor desabilitado',
    'Enable drive': 'Habilite o inversor',
    'Run command': 'Comando de funcionamento',
    'Fault removes run': 'A falha interrompe o funcionamento',
    'Reset and stop': 'Rearme e pare',
    'Run again': 'Acione novamente',
}

TEMPLATES_PT = {
    'Step {current} of {total}': 'Etapa {current} de {total}',
    'Modeled 4-pole synchronous speed: {speed} rpm': 'Velocidade síncrona simulada com 4 polos: {speed} rpm',
    'Imported {count} projects.': '{count} projetos importados.',
    'Question {number}': 'Questão {number}',
    '{correct} / {total} correct · progress saved locally': '{correct} / {total} corretas · progresso salvo localmente',
    'Select by utilization category and {current} A load': 'Selecionar pela categoria de utilização e carga de {current} A',
    'Motor nameplate current; estimate {current} A': 'Corrente da placa do motor; estimativa de {current} A',
    'Interlock conflict: {group}': 'Conflito de intertravamento: {group}',
    'missing_signal:{signal}': 'Sinal ausente: {signal}',
    'reserved_or_duplicate_identifier:{identifier}': 'Identificador reservado ou repetido: {identifier}',
}


def _learning_catalog():
    result = {}
    for name in ("CHAPTERS", "BUILD_STEPS"):
        for source, translated in zip(getattr(learning, name), getattr(learning_pt, name)):
            result.update(zip(source, translated))
    for source, translated in zip(learning.QUESTIONS, learning_pt.QUESTIONS):
        result[source[0]] = translated[0]
        result.update(zip(source[1], translated[1]))
        result[source[3]] = translated[3]
    return result


UI_PT.update({
    "V AC": "V CA", "V DC": "V CC", "A AC": "A CA",
    "AND": "E", "OR": "OU", "NOT": "NÃO",
    " (copy)": " (cópia)",
    "{circuit} project": "Projeto {circuit}",
    "Remove project named {name} from this browser? Export a backup first if needed.": "Remover o projeto {name} deste navegador? Exporte um backup antes, se necessário.",
    "{circuit} · {power} kW · {voltage} V · estimated rated current {current} A": "{circuit} · {power} kW · {voltage} V · corrente nominal estimada {current} A",
    "Electrical controls, motor calculations and circuit simulation in Python. No account required.": "Comandos elétricos, cálculos de motores e simulação de circuitos em Python. Sem necessidade de conta.",
})
PT = {**UI_PT, **_learning_catalog()}
for tag in ("START_FWD", "START_REV", "STAR_DONE", "DELTA_READY", "STAR_TIME", "DEAD_TIME", "RED_REQUEST", "GREEN_REQUEST", "YELLOW_REQUEST", "PHASE_A", "PHASE_B", "PHASE_C", "DRIVE_RUN"):
    PT[tag] = PT[tag.replace("_", " ")]
def match_template(source, value):
    parts = source.split("{")
    if not value.startswith(parts[0]):
        return None
    remaining = value[len(parts[0]):]
    values = {}
    for part in parts[1:]:
        name, separator = part.split("}", 1)
        if separator:
            end = remaining.find(separator)
            if end < 1:
                return None
            values[name] = remaining[:end]
            remaining = remaining[end + len(separator):]
        else:
            if not remaining:
                return None
            values[name] = remaining
            remaining = ""
    return values if not remaining else None


def translate(value, language="en"):
    if not isinstance(value, str) or language != "pt-BR":
        return value
    if value in PT:
        return PT[value]
    for source, target in TEMPLATES_PT.items():
        values = match_template(source, value)
        if values is not None:
            if "group" in values:
                values["group"] = ", ".join(translate(part, language) for part in values["group"].split(", "))
            return target.format(**values)
    for separator in (" · ", " → "):
        if separator in value:
            return separator.join(translate(piece, language) for piece in value.split(separator))
    if "s · " in value:
        prefix, body = value.split("s · ", 1)
        return prefix + "s · " + translate(body, language)
    return value


def signal_label(value, language="en"):
    return translate(value.replace("_", " "), language)


def error_message(value, language="en"):
    message = str(value)
    translated = translate(message, language)
    if translated != message:
        return translated
    if message.startswith(("could not convert string to float", "invalid literal for int")):
        return "Informe um número válido." if language == "pt-BR" else "Enter a valid number."
    if any(part in message for part in ("Expecting ", "Unterminated string", "Extra data", "Invalid control character", "Invalid ", "JSON")):
        return "JSON inválido. Verifique a sintaxe do arquivo ou circuito." if language == "pt-BR" else "Invalid JSON. Check the file or circuit syntax."
    return "Dados inválidos. Verifique os campos e tente novamente." if language == "pt-BR" else "Invalid data. Check the fields and try again."
