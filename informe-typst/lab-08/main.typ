#import "/components/@unsareport/epis-lab/lib.typ": unsa-report, lab-section, code-block

#show: unsa-report.with(
  course_name: "Construcción de Software",
  lab_title: "Diseño de la arquitectura guiada por atributos de calidad — SismoReporta AQP",
  lab_number: "08",
  instructor_name: "Mg. Antonio Arroyo Paz",
  members: (
    "Josue Claudio Quispe Paucar",
    "Diego Alejandro Carbajal Gonzales",
  ),
  year: "2026-B",
  sem_code: "VI",
  presentation_date: "31/10/2026",
  presentation_hour: "No consignada",
  custom_variables: (
    course_abbr: "CS",
    shortnames_chain: "QUISPE-CARBAJAL",
  ),
)

#set text(size: 11pt)
#set par(justify: true, leading: 0.55em)
#v(0.7em)
#include "sections/1-resultados.typ"
#v(0.7em)
#include "sections/2-cuestionario.typ"
#v(0.7em)
#include "sections/3-conclusiones.typ"
