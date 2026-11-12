                "gesto": gesto
            }

            client1.publish(
                "tripletadeo",
                json.dumps(mensaje),
                qos=0,
                retain=False
            )

            time.sleep(0.2)


            # ==========================================
            # ELECCIÓN ALEATORIA DE LA COMPUTADORA
            # ==========================================

            maquina = random.choice(clases)

            st.markdown("### 🤖 Jugada de la computadora")

            st.markdown(
                f'<div class="gesto-detectado">{maquina.upper()}</div>',
                unsafe_allow_html=True
            )


            # ==========================================
            # NORMALIZAR LOS NOMBRES DE LOS GESTOS
            # ==========================================

            jugador_normalizado = gesto.strip().lower()
            maquina_normalizada = maquina.strip().lower()

            equivalencias = {
                "tijeras": "tijera",
                "tijera": "tijera",
                "piedra": "piedra",
                "papel": "papel"
            }

            jugador_normalizado = equivalencias.get(
                jugador_normalizado, jugador_normalizado
            )

            maquina_normalizada = equivalencias.get(
                maquina_normalizada, maquina_normalizada
            )


            # ==========================================
            # REGLAS DEL JUEGO
            # ==========================================

            reglas = {
                "piedra": "tijera",
                "tijera": "papel",
                "papel": "piedra"
            }


            # ==========================================
            # DETERMINAR GANADOR
            # ==========================================

            st.divider()

            st.markdown("### 🏆 Resultado de la ronda")


            if jugador_normalizado not in reglas or maquina_normalizada not in reglas:

                st.markdown(
                    '<div class="resultado resultado-error">No se reconocieron correctamente los nombres de los gestos. Revisa el archivo labels.txt.</div>',
                    unsafe_allow_html=True
                )


            elif jugador_normalizado == maquina_normalizada:

                st.markdown(
                    '<div class="resultado resultado-draw">🤝 ¡EMPATE! Ambos eligieron el mismo gesto.</div>',
                    unsafe_allow_html=True
                )

                # ENVIAR EMPATE AL ESP32
                enviar_resultado("Empate")


            elif reglas[jugador_normalizado] == maquina_normalizada:

                st.markdown(
                    f'<div class="resultado resultado-win">🏆 ¡GANASTE! Tu {gesto} vence a {maquina}.</div>',
                    unsafe_allow_html=True
                )

                # ENVIAR VICTORIA AL ESP32
                enviar_resultado("Gana")


            else:

                st.markdown(
                    f'<div class="resultado resultado-lose">😢 ¡PERDISTE! La {maquina} de la computadora vence a tu {gesto}.</div>',
                    unsafe_allow_html=True
                )

                # ENVIAR DERROTA AL ESP32
                enviar_resultado("Pierde")

                mostrar_consejo_aleatorio()


        else:

            st.warning(
                "No se pudo reconocer el gesto. Intenta nuevamente."
            )
