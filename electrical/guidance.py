from .circuits import input_signals, preset
from .engine import CircuitEngine


STEP_NOTES = {
    "dol": [
        ("The start contact is open; the motor output is off.", "O contato de partida está aberto; a saída do motor está desligada."),
        ("Pressing START energizes the motor output and establishes the holding condition.", "Acionar a partida energiza a saída do motor e estabelece a condição de selo."),
        ("START was released. The auxiliary feedback keeps the motor energized.", "A partida foi solta. A realimentação auxiliar mantém o motor energizado."),
        ("STOP opens the control path and drops the motor output.", "A parada abre o caminho de comando e desliga a saída do motor."),
        ("Releasing STOP restores the permissive, but a new START is required.", "Soltar a parada restabelece o permissivo, mas é necessária uma nova partida.")
    ],
    "reversal": [
        ("Both direction outputs are off; the circuit awaits a start command.", "As saídas dos dois sentidos estão desligadas; o circuito aguarda a partida."),
        ("The forward output energizes. The reverse output remains interlocked.", "A saída do sentido direto energiza. A saída reversa permanece intertravada."),
        ("The forward start was released; its auxiliary feedback maintains the direction.", "A partida direta foi solta; sua realimentação auxiliar mantém o sentido."),
        ("STOP drops the forward output before a direction change.", "A parada desliga a saída direta antes da mudança de sentido."),
        ("The reverse command energizes the reverse output; the forward output stays off.", "O comando reverso energiza a saída reversa; a saída direta permanece desligada."),
        ("The reverse start was released; its holding branch maintains the output.", "A partida reversa foi solta; o ramo de selo mantém a saída."),
        ("STOP removes the holding condition and both direction outputs are off.", "A parada retira a condição de selo e as saídas dos dois sentidos ficam desligadas.")
    ],
    "star_delta": [
        ("Main, star and delta outputs are off; both timers are reset.", "As saídas principal, estrela e triângulo estão desligadas; os dois temporizadores estão reiniciados."),
        ("The main contactor energizes. Star will see this feedback on the next scan.", "O contator principal energiza. A estrela recebe essa realimentação no próximo ciclo."),
        ("Star energizes and its 3-second timer starts; delta remains off.", "A estrela energiza e seu temporizador de 3 segundos começa; o triângulo permanece desligado."),
        ("Star remains energized; 1 of the 3 timer seconds has elapsed.", "A estrela permanece energizada; passou 1 dos 3 segundos do temporizador."),
        ("Star remains energized; 2 of the 3 timer seconds have elapsed.", "A estrela permanece energizada; passaram 2 dos 3 segundos do temporizador."),
        ("The 3-second star timer completes. Star drops on the following scan.", "O temporizador de estrela conclui 3 segundos. A estrela desliga no ciclo seguinte."),
        ("Star opens. Both star and delta are off while the 1-second transition timer starts.", "A estrela abre. Estrela e triângulo ficam desligados enquanto começa a transição de 1 segundo."),
        ("The transition timer completes; delta is enabled for the following scan.", "O temporizador de transição conclui; o triângulo é liberado para o ciclo seguinte."),
        ("Delta energizes with main on and star off; the modeled running connection is established.", "O triângulo energiza com o principal ligado e a estrela desligada; a ligação simulada de regime é estabelecida."),
        ("STOP drops main and cuts the modeled power path. Delta feedback clears on the next scan.", "A parada desliga o principal e corta o caminho de potência simulado. O sinal do triângulo zera no próximo ciclo."),
        ("All outputs and timers are reset. A new start can begin the sequence.", "Todas as saídas e os temporizadores foram reiniciados. Uma nova partida pode iniciar a sequência.")
    ],
    "traffic": [
        ("Only the red lamp is energized; green and yellow remain off.", "Somente a lâmpada vermelha está energizada; verde e amarela permanecem desligadas."),
        ("Red turns off and green turns on in the same output update.", "A vermelha desliga e a verde liga na mesma atualização das saídas."),
        ("Green turns off and yellow turns on; the signal prepares to stop.", "A verde desliga e a amarela liga; a sinalização se prepara para parar."),
        ("Yellow turns off and red turns on, completing the signal cycle.", "A amarela desliga e a vermelha liga, concluindo o ciclo do semáforo.")
    ],
    "phase_loss": [
        ("All three phase permissives are present; the motor still needs a start command.", "Os permissivos das três fases estão presentes; o motor ainda precisa do comando de partida."),
        ("START energizes the motor because every phase permissive is present.", "A partida energiza o motor porque todos os permissivos de fase estão presentes."),
        ("START was released; the motor remains on through its holding feedback.", "A partida foi solta; o motor permanece ligado pela realimentação de selo."),
        ("Phase B was removed. The phase permissive opens and the motor output drops.", "A fase B foi interrompida. O permissivo de fase abre e a saída do motor desliga."),
        ("Phase B was restored, but the holding condition is lost; no automatic restart occurs.", "A fase B foi restabelecida, mas o selo foi perdido; não ocorre nova partida automática."),
        ("A new START energizes the motor with all phase permissives restored.", "Uma nova partida energiza o motor com todos os permissivos de fase restabelecidos.")
    ],
    "vfd": [
        ("The drive is disabled and has no run command; its run output is off.", "O inversor está desabilitado e sem comando de funcionamento; sua saída está desligada."),
        ("Enable is active, but RUN is still absent; the drive remains stopped.", "A habilitação está ativa, mas ainda não há comando de funcionamento; o inversor permanece parado."),
        ("Enable and RUN are active without a fault; the drive run output energizes.", "Habilitação e funcionamento estão ativos sem falha; a saída do inversor energiza."),
        ("The fault input becomes active and blocks the drive run output.", "A entrada de falha fica ativa e bloqueia a saída de funcionamento do inversor."),
        ("The fault was cleared and RUN was removed; the drive awaits another run command.", "A falha foi eliminada e o comando de funcionamento foi retirado; o inversor aguarda um novo comando."),
        ("RUN was requested again with enable active and no fault; the drive resumes running.", "O funcionamento foi solicitado novamente com habilitação ativa e sem falha; o inversor volta a funcionar.")
    ]
}

MANUAL_NOTE = ("The inputs differ from the guided sequence. The output changes below describe this scan.", "As entradas diferem da sequência guiada. As mudanças de saída abaixo descrevem este ciclo.")
CUSTOM_NOTE = ("The custom logic was evaluated using the previous scan's coil states.", "A lógica personalizada foi avaliada com os estados das bobinas do ciclo anterior.")


def step_note(mode, index, inputs, outputs, custom=False, now=None):
    if custom:
        return CUSTOM_NOTE[0]
    model = preset(mode)
    engine = CircuitEngine(model["definition"])
    expected = {key: model["inputs"].get(key, False) for key in input_signals(model["definition"])}
    for position, (_, changes) in enumerate(model["steps"][:index + 1]):
        expected.update(changes)
        engine.scan(expected, position * 1000)
    if inputs != expected or outputs != engine.coils or (now is not None and now != index * 1000):
        return MANUAL_NOTE[0]
    return STEP_NOTES[mode][index][0]


def output_changes(result):
    if result is None:
        return [], []
    on = [item["id"] for item in result["transitions"] if item["energized"]]
    off = [item["id"] for item in result["transitions"] if not item["energized"]]
    return on, off
