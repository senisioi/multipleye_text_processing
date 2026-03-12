# multipleye_text_processing
Code to generate automatic annotations for MultiplEYE languages.

Simply run the following to generate the annotated csv files.

```bash 
# will download the data from 
# https://psycharchives.org/en/item/32f91970-ec71-4983-bbb8-85c2fedfd5a3
./get_data.sh

# will start pulling  images and running the annotations
# size > 20GB (image all contains all the spacy lg models)
docker compose up -d 
``` 

## Cite
```
@inproceedings{kasper2026multipleye,
  title     = {The MultiplEYE Text Corpus: Towards a Diverse and Ever-Expanding Multilingual Text Corpus},
  author    = {Kasper{\.e}, Ramun{\.e} and Bondar, Anna and Nisioi, Sergiu and Stegenwallner-Sch{\"u}tz, Maja and S{\o}ndergaard Knudsen, Hanne B. and Mati{\'c}, Ana and Pavlinu{\v{s}}i{\'c} Vilus, Eva and Klimek-Jankowska, Dorota and Tschirner, Chiara and Soliva, Not Battesta and Jakobi, Deborah N. and Ding, Cui and Abu Romi, Dima and Acarturk, Cengiz and Agdler, Matilda and Alexandru, Anton Marius and Ansari, Mohd Faizan and Arcidiacono, Annalisa and Barisa, Elizabete Ausma Velta and Bautista, Ana and Beinborn, Lisa and Berzak, Yevgeni and Bjelanovi{\'c}, Nedeljka and Bothmann, Anna Isabelle and Brasser, Jan and Cacioli, Caterina and {\c{C}}epani, Anila and Ceple, Ilze and {\c{C}}erpja, Adelina and Chirino, Dal{\'i} and Chrom{\'y}, Jan and Corona Mendozza, Alessandro and de-Dios-Flores, Iria and Din{\c{c}}topal Deniz, Nazik and Do{\v{s}}en, Ana and Elersic, Kristian and Fajardo, Inmaculada and Freibergs, Zigmunds and Ganebnaya, Angelina and Gao, Shan and Gomes, J{\'e}ssica and Greenall, Annjo Klungervik and Haveriku, Alba and He, Miao and Hodivoianu, Anamaria and Hsu, Yu-Yin and Isaksen, Amanda and Janeiro, Andreia and Jensen de L{\'o}pez, Kristine and Jevremovic, Aleksandar and Jovanovi{\'c}, Vojislav and K{\k{e}}dzierska, Hanna and Kharlamov, Nik and Ko{\v{s}}utar, Sara and Kote, Nelda and Kovic, Vanja and Krejtz, Izabela and Krosness, Thyra and Kuvshynova, Oleksandra and Lavy, Eilam and Lion, Ella and {\L}ockiewicz, Marta and L{\~o}o, Kaidi and Luegi, Paula and Marin, Mircea Mihai and Martin, Clara and Matvieieva, Svitlana and M{\'e}zi{\`e}re, Diane C. and M{\'\i}nguez-L{\'o}pez, Xavier and Modina, Valeriia and Motiejunien{\.e}, Jurgita and M{\"u}ller, Marie-Luise and Nasipbek kyzy, Tolgonai and Nasir, Jamal Abdul and Nedergaard, Johanne S. K. and {\"O}zkan, Ay{\c{s}}eg{\"u}l and Paggio, Patrizia and Palmovi{\'c}, Marijan and Panagiotopoulou, Maria Christina and Parola, Alberto and P{\'e}rez, Helena and Petersen, Klaudia and Podlesek, Anja and Posp{\'\i}{\v{s}}ilov{\'a}, Eva and Prauli{\c{n}}a, Marta and Preininger, Mikul{\'a}{\v{s}} and Pung{\u{a}}, Loredana and Rossini, Diego and Rot, {\v{S}}pela and Sani Yahaya, Habib and Sekerina, Irina A. and Skadin{\u{a}}, Anne Gabija and Sol{\'e}-Casals, Jordi and van der Plas, Lonneke and Varjopuro, Saara M. and Varlokosta, Spyridoula and Ver{\'\i}ssimo, Jo{\~a}o and Virtanen, Oskari Juhapekka and Vra{\v{c}}ar, Nemanja and Vulchanova, Mila and Wali, Ahmad Mustapha and Wu, Peizheng and Y{\"u}cel, Nilg{\"u}n and Frank, Stefan and Hollenstein, Nora and J{\"a}ger, Lena A.},
  booktitle = {Proceedings of the 2026 International Conference on Language Resources and Evaluation (LREC 2026)},
  year      = {2026},
  address   = {Rabat, Morocco},
  publisher = {European Language Resources Association and International Committee on Computational Linguistics}
}

@misc{nisioi2026multipleye,
  title        = {The MultiplEYE Text Corpus Data and Materials},
  author       = {Nisioi, Sergiu and Bondar, Anna and Kasper{\.e}, Ramun{\.e} and Stegenwallner-Sch{\"u}tz, Maja},
  year         = {2026},
  month        = mar,
  publisher    = {PsychArchives},
  doi          = {10.23668/psycharchives.21750},
  url          = {https://psycharchives.prod.zpid.org/en/item/32f91970-ec71-4983-bbb8-85c2fedfd5a3},
  language     = {English}
}
```