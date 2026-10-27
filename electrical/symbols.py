from html import escape


SYMBOLS = [
    ("no", "Normally open contact (NO)", "Contato normalmente aberto (NA)", "Closes when actuated; auxiliary example: 13–14.", "Fecha quando acionado; exemplo auxiliar: 13–14."),
    ("nc", "Normally closed contact (NC)", "Contato normalmente fechado (NF)", "Opens when actuated; auxiliary example: 21–22.", "Abre quando acionado; exemplo auxiliar: 21–22."),
    ("coil", "Relay / contactor coil", "Bobina de relé / contator", "Electromagnetic control; coil terminals: A1–A2.", "Comando eletromagnético; terminais da bobina: A1–A2."),
    ("isolator", "Disconnector", "Seccionadora", "Provides isolation when selected for that purpose.", "Proporciona isolamento quando selecionada para essa finalidade."),
    ("breaker", "Circuit-breaker", "Disjuntor", "Switching device with automatic fault interruption.", "Dispositivo de manobra com interrupção automática de falhas."),
    ("fuse", "Fuse", "Fusível", "Melting element interrupts an overcurrent.", "O elemento fusível interrompe uma sobrecorrente."),
    ("relay", "Overcurrent relay", "Relé de sobrecorrente", "I> indicates an overcurrent measuring function.", "I> indica uma função de medição de sobrecorrente."),
    ("motor", "Three-phase motor", "Motor trifásico", "M identifies a motor; 3~ indicates three-phase AC.", "M identifica um motor; 3~ indica corrente alternada trifásica."),
    ("lamp", "Signal lamp", "Lâmpada de sinalização", "Indicates an operating state; used by the traffic sequence.", "Indica um estado de operação; usada na sequência do semáforo."),
    ("junction", "Connection of conductors", "Conexão de condutores", "A solid dot marks an electrical junction.", "Um ponto preenchido indica uma conexão elétrica."),
    ("pe", "Protective earth (PE)", "Terra de proteção (PE)", "Protective earthing connection; distinct from neutral N.", "Conexão de aterramento de proteção; diferente do neutro N."),
    ("converter", "Converter / drive", "Conversor / inversor", "AC-to-AC conversion represents the drive function here.", "A conversão CA–CA representa aqui a função do inversor."),
    ("timer", "On-delay timer (TON)", "Temporizador com retardo na energização (TON)", "IEC 61131-3 block: IN input, PT preset, Q output, ET elapsed time.", "Bloco IEC 61131-3: IN entrada, PT tempo ajustado, Q saída, ET tempo decorrido.")
]

GLYPHS = {
    "no": '<path d="M2 30H22M22 30 55 10M55 30H82"/><circle cx="22" cy="30" r="2"/><circle cx="55" cy="30" r="2"/>',
    "nc": '<path d="M2 34H22L55 16M55 16V31M55 24H82"/><circle cx="22" cy="34" r="2"/>',
    "coil": '<path d="M2 28H15M69 28H82"/><rect x="15" y="16" width="54" height="24"/>',
    "isolator": '<path d="M2 32H22L55 10M55 32H82"/><rect x="52" y="29" width="6" height="6"/>',
    "breaker": '<path d="M2 34H22L55 10M55 34H82M17 29 27 39M17 39 27 29"/>',
    "fuse": '<path d="M2 28H82"/><rect x="20" y="18" width="44" height="20"/>',
    "relay": '<path d="M2 28H15M69 28H82"/><rect x="15" y="10" width="54" height="36"/><text x="42" y="34" text-anchor="middle" class="symbol-letter">I&gt;</text>',
    "motor": '<path d="M42 0V7M42 49V56"/><circle cx="42" cy="28" r="21"/><text x="42" y="29" text-anchor="middle" class="symbol-letter">M</text><text x="42" y="42" text-anchor="middle" class="symbol-small">3~</text>',
    "lamp": '<path d="M2 28H23M61 28H82M29 15 55 41M29 41 55 15"/><circle cx="42" cy="28" r="19"/>',
    "junction": '<path d="M2 28H82M42 4V52"/><circle cx="42" cy="28" r="4" fill="currentColor"/>',
    "pe": '<path d="M42 0V24M26 24H58M31 31H53M36 38H48"/><circle cx="42" cy="28" r="23"/>',
    "converter": '<path d="M2 28H17M67 28H82M17 48 67 8"/><rect x="17" y="8" width="50" height="40"/><text x="30" y="25" text-anchor="middle" class="symbol-letter">~</text><text x="54" y="43" text-anchor="middle" class="symbol-letter">~</text>',
    "timer": '<rect x="18" y="3" width="48" height="50"/><path d="M2 24H18M2 41H18M66 24H82M66 41H82"/><text x="42" y="16" text-anchor="middle" class="symbol-small">TON</text><text x="22" y="28" class="symbol-tiny">IN</text><text x="22" y="45" class="symbol-tiny">PT</text><text x="61" y="28" text-anchor="end" class="symbol-tiny">Q</text><text x="61" y="45" text-anchor="end" class="symbol-tiny">ET</text>'
}


def symbol_svg(key, label):
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 84 56" role="img" aria-label="' + escape(label, quote=True) + '" class="electrical-symbol"><g fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="square" stroke-linejoin="miter">' + GLYPHS[key] + '</g></svg>'
