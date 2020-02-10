#!/usr/bin/env bash

set -x

# download main data
curl -o "bibtag20-index.json" -k "https://www.professionalabstracts.com/api/iplanner/index.php?conf=dbt2020&method=get&model=index"
sleep 2

# list of all session ids found by
# jq ".sessions" bibtag20-index.json | grep '"id"' > sessionids
# and then some text search and replace to bring this in the form needed for the for loop here

# download details of all sessions
for id in
# comment previous line and uncomment next line to activate
#for id in 62 118 75 79 101 122 117 114 173 154 15 28 151 170 31 186 210 199 196 44 47 40 219 59 98 92 35 109 110 36 155 218 100 82 217 17 178 188 3 209 74 48 2 195 88 223 96 69 221 9 202 136 207 125 60 182 130 198 180 212 225 177 4 50 73 239 244 157 232 58 105 67 38 95 41 45 164 149 107 204 184 147 190 160 226 63 53 21 10 240 233 245 106 87 220 93 108 128 80 22 51 163 165 141 43 6 152 142 193 55 8 16 70 42 29 241 242 71 66 222 111 76 116 224 89 158 166 37 52 156 150 200 189 57 18 11 25 153 235 205 243 81 102 127 61 77 12 27 86 83 174 192 64 7 185 143 167 227 214 228 169 237 129 208 121 203 26 172 145 20 54 131 181 161 187 229 236 238 234 246 72 34 126 85 104 119 46 97 13 144 162 49 65 179 19 176 159 230 124 99 91 115 39 112 68 84 5 140 171 33 14 23 168 191 231 94 123 90 113 134 216 201 120 24 78 103 56 183 175 30 139 146 194
do
    curl -o "s${id}.json" -k "https://www.professionalabstracts.com/api/iplanner/index.php?conf=dbt2020&method=get&model=sessions&params[sids]=${id}"
    sleep 2
done

# grep 'event id="p' ../output.xml > presentationsids

# download details of all presentations
for id in
# comment previous line and uncomment next line to activate
#for id in 410 185 186 187 188 189 112 113 114 115 23 24 25 26 27 88 89 90 91 37 38 39 40 41 123 124 125 126 127 154 153 152 155 201 202 203 156 157 158 159 181 182 183 184 398 165 166 167 168 357 257 316 298 297 119 120 121 122 247 52 53 54 291 313 235 255 321 329 331 362 338 269 361 282 285 401 404 397 70 71 72 204 279 141 142 143 144 138 139 140 73 74 75 76 105 106 107 373 92 93 94 95 160 161 162 372 148 149 150 151 28 29 30 407 224 225 226 227 343 344 345 263 268 77 78 79 416 308 306 301 358 419 307 309 214 215 216 145 146 147 420 259 281 352 353 354 403 274 325 327 399 299 423 413 293 289 337 333 290 339 323 303 336 332 364 376 378 286 320 288 271 287 270 276 275 411 267 412 284 273 409 272 261 280 386 300 251 296 355 395 102 103 104 206 42 43 44 45 178 179 180 240 375 383 46 47 48 49 50 51 211 212 213 131 132 133 228 229 230 116 117 118 221 222 223 360 217 218 219 220 85 86 87 198 199 342 66 67 68 69 175 176 177 31 32 421 346 347 348 134 135 136 137 406 190 191 192 193 163 164 244 402 265 61 62 63 64 65 108 109 110 111 58 59 60 55 56 57 205 424 232 405 317 315 295 292 335 418 305 314 283 238 266 408 231 233 328 422 322 417 324 236 400 310 304 319 311 425 330 302 334 366 379 380 381 382 312 384 385 96 97 98 99 100 101 207 208 209 210 80 81 82 83 84 359 169 170 171 172 173 174 415 368 194 195 196 197 243 34 35 36 340 128 129 130 341 277 326 318 253 414 294
do
    curl -o "p${id}.json" -k "https://www.professionalabstracts.com/api/iplanner/index.php?conf=dbt2020&method=get&model=presentation&params[pid]=${id}"
    sleep 2
done
set +x
