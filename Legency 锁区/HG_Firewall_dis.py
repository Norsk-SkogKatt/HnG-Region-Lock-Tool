# HG服务器锁定v2.1 - 字节码反汇编
# 由Python marshal + dis生成


# ====== log_init ======
 67           0 RESUME                   0

 69           2 LOAD_GLOBAL              0 (os)
             12 LOAD_ATTR                2 (path)
             32 LOAD_ATTR                5 (NULL|self + join)
             52 LOAD_GLOBAL              7 (NULL + _get_base_dir)
             62 CALL                     0
             70 LOAD_CONST               1 ('HG_lock.log')
             72 CALL                     2
             80 STORE_GLOBAL             4 (LOG_FILE)

 71          82 NOP

 72          84 LOAD_GLOBAL             11 (NULL + open)
             94 LOAD_GLOBAL              8 (LOG_FILE)
            104 LOAD_CONST               2 ('w')
            106 LOAD_CONST               3 ('utf-8')
            108 KW_NAMES                 4 (('encoding',))
            110 CALL                     3
            118 BEFORE_WITH
            120 STORE_FAST               0 (f)

 73         122 LOAD_FAST                0 (f)
            124 LOAD_ATTR               13 (NULL|self + write)
            144 LOAD_CONST               5 ('=== HG 伺服器鎖定 v2.0 日誌 ===\n')
            146 CALL                     1
            154 POP_TOP

 74         156 LOAD_FAST                0 (f)
            158 LOAD_ATTR               13 (NULL|self + write)
            178 LOAD_CONST               6 ('啟動時間: ')
            180 LOAD_GLOBAL             14 (datetime)
            190 LOAD_ATTR               14 (datetime)
            210 LOAD_ATTR               17 (NULL|self + now)
            230 CALL                     0
            238 LOAD_ATTR               19 (NULL|self + strftime)
            258 LOAD_CONST               7 ('%Y-%m-%d %H:%M:%S')
            260 CALL                     1
            268 FORMAT_VALUE             0
            270 LOAD_CONST               8 ('\n\n')
            272 BUILD_STRING             3
            274 CALL                     1
            282 POP_TOP

 72         284 LOAD_CONST               0 (None)
            286 LOAD_CONST               0 (None)
            288 LOAD_CONST               0 (None)
            290 CALL                     2
            298 POP_TOP
            300 RETURN_CONST             0 (None)
        >>  302 PUSH_EXC_INFO
            304 WITH_EXCEPT_START
            306 POP_JUMP_IF_TRUE         1 (to 310)
            308 RERAISE                  2
        >>  310 POP_TOP
            312 POP_EXCEPT
            314 POP_TOP
            316 POP_TOP
            318 RETURN_CONST             0 (None)
        >>  320 COPY                     3
            322 POP_EXCEPT
            324 RERAISE                  1
        >>  326 PUSH_EXC_INFO

 75         328 POP_TOP

 76         330 POP_EXCEPT
            332 RETURN_CONST             0 (None)
        >>  334 COPY                     3
            336 POP_EXCEPT
            338 RERAISE                  1
ExceptionTable:
  84 to 118 -> 326 [0]
  120 to 282 -> 302 [1] lasti
  284 to 298 -> 326 [0]
  302 to 310 -> 320 [3] lasti
  312 to 316 -> 326 [0]
  320 to 324 -> 326 [0]
  326 to 328 -> 334 [1] lasti


# ====== load_config ======
103           0 RESUME                   0

104           2 LOAD_GLOBAL              1 (NULL + _config_path)
             12 CALL                     0
             20 STORE_FAST               0 (fp)

105          22 LOAD_GLOBAL              2 (os)
             32 LOAD_ATTR                4 (path)
             52 LOAD_ATTR                7 (NULL|self + isfile)
             72 LOAD_FAST                0 (fp)
             74 CALL                     1
             82 POP_JUMP_IF_TRUE         2 (to 88)

106          84 BUILD_MAP                0
             86 RETURN_VALUE

107     >>   88 NOP

108          90 LOAD_GLOBAL              9 (NULL + open)
            100 LOAD_FAST                0 (fp)
            102 LOAD_CONST               1 ('r')
            104 LOAD_CONST               2 ('utf-8')
            106 KW_NAMES                 3 (('encoding',))
            108 CALL                     3
            116 BEFORE_WITH
            118 STORE_FAST               1 (f)

109         120 LOAD_GLOBAL             11 (NULL + json)
            130 LOAD_ATTR               12 (load)
            150 LOAD_FAST                1 (f)
            152 CALL                     1

108         160 SWAP                     2
            162 LOAD_CONST               0 (None)
            164 LOAD_CONST               0 (None)
            166 LOAD_CONST               0 (None)
            168 CALL                     2
            176 POP_TOP
            178 RETURN_VALUE
        >>  180 PUSH_EXC_INFO
            182 WITH_EXCEPT_START
            184 POP_JUMP_IF_TRUE         1 (to 188)
            186 RERAISE                  2
        >>  188 POP_TOP
            190 POP_EXCEPT
            192 POP_TOP
            194 POP_TOP
            196 RETURN_CONST             0 (None)
        >>  198 COPY                     3
            200 POP_EXCEPT
            202 RERAISE                  1
        >>  204 PUSH_EXC_INFO

110         206 POP_TOP

111         208 BUILD_MAP                0
            210 SWAP                     2
            212 POP_EXCEPT
            214 RETURN_VALUE
        >>  216 COPY                     3
            218 POP_EXCEPT
            220 RERAISE                  1
ExceptionTable:
  90 to 116 -> 204 [0]
  118 to 158 -> 180 [1] lasti
  160 to 176 -> 204 [0]
  180 to 188 -> 198 [3] lasti
  190 to 194 -> 204 [0]
  198 to 202 -> 204 [0]
  204 to 210 -> 216 [1] lasti


# ====== save_config ======
113           0 RESUME                   0

114           2 LOAD_GLOBAL              1 (NULL + _config_path)
             12 CALL                     0
             20 STORE_FAST               2 (fp)

115          22 NOP

116          24 LOAD_GLOBAL              3 (NULL + open)
             34 LOAD_FAST                2 (fp)
             36 LOAD_CONST               1 ('w')
             38 LOAD_CONST               2 ('utf-8')
             40 KW_NAMES                 3 (('encoding',))
             42 CALL                     3
             50 BEFORE_WITH
             52 STORE_FAST               3 (f)

117          54 LOAD_GLOBAL              5 (NULL + json)
             64 LOAD_ATTR                6 (dump)
             84 LOAD_FAST                0 (hn_path)
             86 LOAD_FAST                1 (last_mode)
             88 LOAD_CONST               4 (('hn_path', 'last_mode'))
             90 BUILD_CONST_KEY_MAP      2
             92 LOAD_FAST                3 (f)
             94 LOAD_CONST               5 (False)
             96 LOAD_CONST               6 (2)
             98 KW_NAMES                 7 (('ensure_ascii', 'indent'))
            100 CALL                     4
            108 POP_TOP

116         110 LOAD_CONST               0 (None)
            112 LOAD_CONST               0 (None)
            114 LOAD_CONST               0 (None)
            116 CALL                     2
            124 POP_TOP
            126 RETURN_CONST             0 (None)
        >>  128 PUSH_EXC_INFO
            130 WITH_EXCEPT_START
            132 POP_JUMP_IF_TRUE         1 (to 136)
            134 RERAISE                  2
        >>  136 POP_TOP
            138 POP_EXCEPT
            140 POP_TOP
            142 POP_TOP
            144 RETURN_CONST             0 (None)
        >>  146 COPY                     3
            148 POP_EXCEPT
            150 RERAISE                  1
        >>  152 PUSH_EXC_INFO

118         154 POP_TOP

119         156 POP_EXCEPT
            158 RETURN_CONST             0 (None)
        >>  160 COPY                     3
            162 POP_EXCEPT
            164 RERAISE                  1
ExceptionTable:
  24 to 50 -> 152 [0]
  52 to 108 -> 128 [1] lasti
  110 to 124 -> 152 [0]
  128 to 136 -> 146 [3] lasti
  138 to 142 -> 152 [0]
  146 to 150 -> 152 [0]
  152 to 154 -> 160 [1] lasti


# ====== is_admin ======
122           0 RESUME                   0

123           2 NOP

124           4 LOAD_GLOBAL              0 (ctypes)
             14 LOAD_ATTR                2 (windll)
             34 LOAD_ATTR                4 (shell32)
             54 LOAD_ATTR                7 (NULL|self + IsUserAnAdmin)
             74 CALL                     0
             82 LOAD_CONST               1 (0)
             84 COMPARE_OP              55 (!=)
             88 RETURN_VALUE
        >>   90 PUSH_EXC_INFO

125          92 POP_TOP

126          94 POP_EXCEPT
             96 RETURN_CONST             2 (False)
        >>   98 COPY                     3
            100 POP_EXCEPT
            102 RERAISE                  1
ExceptionTable:
  4 to 86 -> 90 [0]
  90 to 92 -> 98 [1] lasti


# ====== run_as_admin ======
128           0 RESUME                   0

129           2 LOAD_GLOBAL              1 (NULL + getattr)
             12 LOAD_GLOBAL              2 (sys)
             22 LOAD_CONST               1 ('frozen')
             24 LOAD_CONST               2 (False)
             26 CALL                     3
             34 POP_JUMP_IF_FALSE       17 (to 70)

130          36 LOAD_GLOBAL              2 (sys)
             46 LOAD_ATTR                4 (executable)
             66 STORE_FAST               0 (exe_path)
             68 JUMP_FORWARD            48 (to 166)

132     >>   70 LOAD_GLOBAL              6 (os)
             80 LOAD_ATTR                8 (path)
            100 LOAD_ATTR               11 (NULL|self + abspath)
            120 LOAD_GLOBAL              2 (sys)
            130 LOAD_ATTR               12 (argv)
            150 LOAD_CONST               3 (0)
            152 BINARY_SUBSCR
            156 CALL                     1
            164 STORE_FAST               0 (exe_path)

133     >>  166 LOAD_GLOBAL             14 (ctypes)
            176 LOAD_ATTR               16 (windll)
            196 LOAD_ATTR               18 (shell32)
            216 LOAD_ATTR               21 (NULL|self + ShellExecuteW)
            236 LOAD_CONST               0 (None)
            238 LOAD_CONST               4 ('runas')
            240 LOAD_FAST                0 (exe_path)
            242 LOAD_CONST               5 (' ')
            244 LOAD_ATTR               23 (NULL|self + join)
            264 LOAD_GLOBAL              2 (sys)
            274 LOAD_ATTR               12 (argv)
            294 LOAD_CONST               6 (1)
            296 LOAD_CONST               0 (None)
            298 BINARY_SLICE
            300 CALL                     1
            308 LOAD_CONST               0 (None)
            310 LOAD_CONST               6 (1)
            312 CALL                     6
            320 POP_TOP

134         322 LOAD_GLOBAL              3 (NULL + sys)
            332 LOAD_ATTR               24 (exit)
            352 LOAD_CONST               3 (0)
            354 CALL                     1
            362 POP_TOP
            364 RETURN_CONST             0 (None)


# ====== run_netsh ======
137           0 RESUME                   0

139           2 NOP

140           4 LOAD_GLOBAL              1 (NULL + subprocess)
             14 LOAD_ATTR                2 (run)

141          34 BUILD_LIST               0
             36 LOAD_CONST               1 (('netsh', 'advfirewall', 'firewall'))
             38 LIST_EXTEND              1
             40 LOAD_FAST                0 (args)
             42 BINARY_OP                0 (+)

142          46 LOAD_CONST               2 (True)

140          48 KW_NAMES                 3 (('capture_output',))
             50 CALL                     2
             58 STORE_FAST               1 (result)

144          60 LOAD_FAST                1 (result)
             62 LOAD_ATTR                4 (returncode)
             82 LOAD_CONST               4 (0)
             84 COMPARE_OP              55 (!=)
             88 POP_JUMP_IF_FALSE       93 (to 276)

145          90 LOAD_FAST                1 (result)
             92 LOAD_ATTR                6 (stderr)
            112 COPY                     1
            114 POP_JUMP_IF_TRUE         2 (to 120)
            116 POP_TOP
            118 LOAD_CONST               5 (b'')
        >>  120 LOAD_ATTR                9 (NULL|self + decode)
            140 LOAD_CONST               6 ('utf-8')
            142 LOAD_CONST               7 ('replace')
            144 KW_NAMES                 8 (('errors',))
            146 CALL                     2
            154 LOAD_ATTR               11 (NULL|self + strip)
            174 CALL                     0
            182 STORE_FAST               2 (err)

146         184 LOAD_FAST                2 (err)
            186 POP_JUMP_IF_FALSE       18 (to 224)
            188 LOAD_CONST               9 ('netsh 返回 ')
            190 LOAD_FAST                1 (result)
            192 LOAD_ATTR                4 (returncode)
            212 FORMAT_VALUE             0
            214 LOAD_CONST              10 (': ')
            216 LOAD_FAST                2 (err)
            218 FORMAT_VALUE             0
            220 BUILD_STRING             4
            222 JUMP_FORWARD            14 (to 252)
        >>  224 LOAD_CONST               9 ('netsh 返回 ')
            226 LOAD_FAST                1 (result)
            228 LOAD_ATTR                4 (returncode)
            248 FORMAT_VALUE             0
            250 BUILD_STRING             2
        >>  252 STORE_FAST               3 (msg)

147         254 LOAD_GLOBAL             13 (NULL + log_error)
            264 LOAD_FAST                3 (msg)
            266 CALL                     1
            274 POP_TOP

148     >>  276 LOAD_FAST                1 (result)
            278 LOAD_ATTR               14 (stdout)
            298 POP_JUMP_IF_FALSE       33 (to 366)
            300 LOAD_FAST                1 (result)
            302 LOAD_ATTR               14 (stdout)
            322 COPY                     1
            324 POP_JUMP_IF_TRUE         2 (to 330)
            326 POP_TOP
            328 LOAD_CONST               5 (b'')
        >>  330 LOAD_ATTR                9 (NULL|self + decode)
            350 LOAD_CONST               6 ('utf-8')
            352 LOAD_CONST               7 ('replace')
            354 KW_NAMES                 8 (('errors',))
            356 CALL                     2
            364 RETURN_VALUE
        >>  366 LOAD_CONST              11 ('')
            368 RETURN_VALUE
        >>  370 PUSH_EXC_INFO

149         372 LOAD_GLOBAL             16 (Exception)
            382 CHECK_EXC_MATCH
            384 POP_JUMP_IF_FALSE       24 (to 434)
            386 STORE_FAST               4 (e)

150         388 LOAD_GLOBAL             13 (NULL + log_error)
            398 LOAD_CONST              12 ('netsh 異常: ')
            400 LOAD_FAST                4 (e)
            402 FORMAT_VALUE             0
            404 BUILD_STRING             2
            406 CALL                     1
            414 POP_TOP

151         416 POP_EXCEPT
            418 LOAD_CONST              13 (None)
            420 STORE_FAST               4 (e)
            422 DELETE_FAST              4 (e)
            424 RETURN_CONST            11 ('')
        >>  426 LOAD_CONST              13 (None)
            428 STORE_FAST               4 (e)
            430 DELETE_FAST              4 (e)
            432 RERAISE                  1

149     >>  434 RERAISE                  0
        >>  436 COPY                     3
            438 POP_EXCEPT
            440 RERAISE                  1
ExceptionTable:
  4 to 362 -> 370 [0]
  366 to 366 -> 370 [0]
  370 to 386 -> 436 [1] lasti
  388 to 414 -> 426 [1] lasti
  426 to 434 -> 436 [1] lasti


# ====== get_rule_lines ======
153           0 RESUME                   0

156           2 NOP

157           4 LOAD_CONST               1 ("(Get-NetFirewallRule | Where-Object { $_.DisplayName -like '")
              6 LOAD_FAST                0 (keyword)
              8 FORMAT_VALUE             0
             10 LOAD_CONST               2 ("*' }).DisplayName")
             12 BUILD_STRING             3
             14 STORE_FAST               1 (ps_code)

158          16 LOAD_GLOBAL              1 (NULL + subprocess)
             26 LOAD_ATTR                2 (run)

159          46 LOAD_CONST               3 ('powershell')
             48 LOAD_CONST               4 ('-NoProfile')
             50 LOAD_CONST               5 ('-Command')
             52 LOAD_FAST                1 (ps_code)
             54 BUILD_LIST               4

160          56 LOAD_CONST               6 (True)
             58 LOAD_GLOBAL              0 (subprocess)
             68 LOAD_ATTR                4 (CREATE_NO_WINDOW)

158          88 KW_NAMES                 7 (('capture_output', 'creationflags'))
             90 CALL                     3
             98 STORE_FAST               2 (result)

162         100 LOAD_FAST                2 (result)
            102 LOAD_ATTR                6 (stdout)
            122 COPY                     1
            124 POP_JUMP_IF_TRUE         2 (to 130)
            126 POP_TOP
            128 LOAD_CONST               8 (b'')
        >>  130 LOAD_ATTR                9 (NULL|self + decode)
            150 LOAD_CONST               9 ('utf-8')
            152 LOAD_CONST              10 ('replace')
            154 KW_NAMES                11 (('errors',))
            156 CALL                     2
            164 LOAD_ATTR               11 (NULL|self + strip)
            184 CALL                     0
            192 STORE_FAST               3 (output)

163         194 LOAD_FAST                3 (output)
            196 POP_JUMP_IF_FALSE       62 (to 322)

164         198 LOAD_FAST                3 (output)
            200 LOAD_ATTR               13 (NULL|self + splitlines)
            220 CALL                     0
            228 GET_ITER
            230 LOAD_FAST_AND_CLEAR      4 (n)
            232 SWAP                     2
            234 BUILD_LIST               0
            236 SWAP                     2
        >>  238 FOR_ITER                35 (to 312)
            242 STORE_FAST               4 (n)
            244 LOAD_FAST                4 (n)
            246 LOAD_ATTR               11 (NULL|self + strip)
            266 CALL                     0
            274 POP_JUMP_IF_TRUE         1 (to 278)
            276 JUMP_BACKWARD           20 (to 238)
        >>  278 LOAD_FAST                4 (n)
            280 LOAD_ATTR               11 (NULL|self + strip)
            300 CALL                     0
            308 LIST_APPEND              2
            310 JUMP_BACKWARD           37 (to 238)
        >>  312 END_FOR
            314 STORE_FAST               5 (names)
            316 STORE_FAST               4 (n)

165         318 LOAD_FAST                5 (names)
            320 RETURN_VALUE

163     >>  322 NOP

170     >>  324 LOAD_GLOBAL             15 (NULL + run_netsh)
            334 BUILD_LIST               0
            336 LOAD_CONST              12 (('show', 'rule', 'name=all'))
            338 LIST_EXTEND              1
            340 CALL                     1
            348 STORE_FAST               3 (output)

171         350 BUILD_LIST               0
            352 STORE_FAST               6 (lines)

172         354 LOAD_FAST                3 (output)
            356 LOAD_ATTR               13 (NULL|self + splitlines)
            376 CALL                     0
            384 GET_ITER
        >>  386 FOR_ITER               104 (to 598)
            390 STORE_FAST               7 (line)

173         392 LOAD_FAST                7 (line)
            394 LOAD_ATTR               11 (NULL|self + strip)
            414 CALL                     0
            422 STORE_FAST               8 (stripped)

174         424 LOAD_FAST                0 (keyword)
            426 LOAD_FAST                8 (stripped)
            428 CONTAINS_OP              1
            430 POP_JUMP_IF_TRUE         4 (to 440)
            432 LOAD_CONST              13 (':')
            434 LOAD_FAST                8 (stripped)
            436 CONTAINS_OP              1
            438 POP_JUMP_IF_FALSE        1 (to 442)

175     >>  440 JUMP_BACKWARD           28 (to 386)

176     >>  442 LOAD_FAST                8 (stripped)
            444 LOAD_ATTR               17 (NULL|self + split)
            464 LOAD_CONST              13 (':')
            466 LOAD_CONST              14 (1)
            468 CALL                     2
            476 STORE_FAST               9 (parts)

177         478 LOAD_GLOBAL             19 (NULL + len)
            488 LOAD_FAST                9 (parts)
            490 CALL                     1
            498 LOAD_CONST              15 (2)
            500 COMPARE_OP              40 (==)
            504 POP_JUMP_IF_TRUE         1 (to 508)
            506 JUMP_BACKWARD           61 (to 386)

178     >>  508 LOAD_FAST                9 (parts)
            510 LOAD_CONST              14 (1)
            512 BINARY_SUBSCR
            516 LOAD_ATTR               11 (NULL|self + strip)
            536 CALL                     0
            544 STORE_FAST              10 (name)

179         546 LOAD_FAST               10 (name)
            548 POP_JUMP_IF_TRUE         1 (to 552)
            550 JUMP_BACKWARD           83 (to 386)
        >>  552 LOAD_FAST                0 (keyword)
            554 LOAD_FAST               10 (name)
            556 CONTAINS_OP              0
            558 POP_JUMP_IF_TRUE         1 (to 562)
            560 JUMP_BACKWARD           88 (to 386)

180     >>  562 LOAD_FAST                6 (lines)
            564 LOAD_ATTR               21 (NULL|self + append)
            584 LOAD_FAST               10 (name)
            586 CALL                     1
            594 POP_TOP
            596 JUMP_BACKWARD          106 (to 386)

172     >>  598 END_FOR

181         600 LOAD_FAST                6 (lines)
            602 RETURN_VALUE
        >>  604 SWAP                     2
            606 POP_TOP

164         608 SWAP                     2
            610 STORE_FAST               4 (n)
            612 RERAISE                  0
        >>  614 PUSH_EXC_INFO

166         616 POP_TOP

167         618 POP_EXCEPT
            620 JUMP_BACKWARD          149 (to 324)
        >>  622 COPY                     3
            624 POP_EXCEPT
            626 RERAISE                  1
ExceptionTable:
  4 to 232 -> 614 [0]
  234 to 274 -> 604 [2]
  278 to 312 -> 604 [2]
  314 to 318 -> 614 [0]
  604 to 612 -> 614 [0]
  614 to 616 -> 622 [1] lasti


# ====== remove_old_v1_rules ======
184           0 RESUME                   0

185           2 LOAD_CONST               1 (0)
              4 LOAD_CONST               0 (None)
              6 IMPORT_NAME              0 (re)
              8 STORE_FAST               0 (re)

186          10 LOAD_GLOBAL              3 (NULL + print)
             20 LOAD_CONST               2 ('[*] 正在檢查 v1.1 舊版規則…')
             22 CALL                     1
             30 POP_TOP

187          32 LOAD_GLOBAL              5 (NULL + run_netsh)
             42 BUILD_LIST               0
             44 LOAD_CONST               3 (('show', 'rule', 'name=all'))
             46 LIST_EXTEND              1
             48 CALL                     1
             56 STORE_FAST               1 (rules)

188          58 LOAD_CONST               1 (0)
             60 STORE_FAST               2 (count)

189          62 LOAD_FAST                1 (rules)
             64 LOAD_ATTR                7 (NULL|self + splitlines)
             84 CALL                     0
             92 GET_ITER
        >>   94 FOR_ITER               137 (to 372)
             98 STORE_FAST               3 (line)

190         100 LOAD_FAST                0 (re)
            102 LOAD_ATTR                9 (NULL|self + search)
            122 LOAD_CONST               4 ('HG-[\\d\\.]+\\([A-Za-z-]+\\)-(TCP|UDP)$')
            124 LOAD_FAST                3 (line)
            126 LOAD_ATTR               11 (NULL|self + strip)
            146 CALL                     0
            154 CALL                     2
            162 POP_JUMP_IF_TRUE         1 (to 166)
            164 JUMP_BACKWARD           36 (to 94)

191     >>  166 LOAD_FAST                3 (line)
            168 LOAD_ATTR               11 (NULL|self + strip)
            188 CALL                     0
            196 LOAD_ATTR               13 (NULL|self + split)
            216 LOAD_CONST               5 (':')
            218 LOAD_CONST               6 (1)
            220 CALL                     2
            228 STORE_FAST               4 (parts)

192         230 LOAD_GLOBAL             15 (NULL + len)
            240 LOAD_FAST                4 (parts)
            242 CALL                     1
            250 LOAD_CONST               7 (2)
            252 COMPARE_OP              40 (==)
            256 POP_JUMP_IF_TRUE         1 (to 260)
            258 JUMP_BACKWARD           83 (to 94)

193     >>  260 LOAD_FAST                4 (parts)
            262 LOAD_CONST               6 (1)
            264 BINARY_SUBSCR
            268 LOAD_ATTR               11 (NULL|self + strip)
            288 CALL                     0
            296 STORE_FAST               5 (name)

194         298 LOAD_GLOBAL              3 (NULL + print)
            308 LOAD_CONST               8 ('  [-] ')
            310 LOAD_FAST                5 (name)
            312 FORMAT_VALUE             0
            314 BUILD_STRING             2
            316 CALL                     1
            324 POP_TOP

195         326 LOAD_GLOBAL              5 (NULL + run_netsh)
            336 LOAD_CONST               9 ('delete')
            338 LOAD_CONST              10 ('rule')
            340 LOAD_CONST              11 ('name=')
            342 LOAD_FAST                5 (name)
            344 FORMAT_VALUE             0
            346 BUILD_STRING             2
            348 BUILD_LIST               3
            350 CALL                     1
            358 POP_TOP

196         360 LOAD_FAST                2 (count)
            362 LOAD_CONST               6 (1)
            364 BINARY_OP               13 (+=)
            368 STORE_FAST               2 (count)
            370 JUMP_BACKWARD          139 (to 94)

189     >>  372 END_FOR

197         374 LOAD_FAST                2 (count)
            376 LOAD_CONST               1 (0)
            378 COMPARE_OP              68 (>)
            382 POP_JUMP_IF_FALSE       31 (to 446)

198         384 LOAD_GLOBAL              3 (NULL + print)
            394 LOAD_CONST              12 ('  [✓] 已清除 ')
            396 LOAD_FAST                2 (count)
            398 FORMAT_VALUE             0
            400 LOAD_CONST              13 (' 條舊版規則')
            402 BUILD_STRING             3
            404 CALL                     1
            412 POP_TOP

199         414 LOAD_GLOBAL             17 (NULL + log_action)
            424 LOAD_CONST              14 ('清除 ')
            426 LOAD_FAST                2 (count)
            428 FORMAT_VALUE             0
            430 LOAD_CONST              15 (' 條 v1.1 舊版規則')
            432 BUILD_STRING             3
            434 CALL                     1
            442 POP_TOP
            444 RETURN_CONST             0 (None)

201     >>  446 LOAD_GLOBAL              3 (NULL + print)
            456 LOAD_CONST              16 ('  [-] 沒有舊版規則')
            458 CALL                     1
            466 POP_TOP

202         468 LOAD_GLOBAL             19 (NULL + log_info)
            478 LOAD_CONST              17 ('無 v1.1 舊版規則')
            480 CALL                     1
            488 POP_TOP
            490 RETURN_CONST             0 (None)


# ====== remove_legacy_global_rule ======
205           0 RESUME                   0

206           2 LOAD_GLOBAL              1 (NULL + run_netsh)
             12 BUILD_LIST               0
             14 LOAD_CONST               1 (('show', 'rule', 'name=HG_internet_disable_rule_output'))
             16 LIST_EXTEND              1
             18 CALL                     1
             26 STORE_FAST               0 (output)

207          28 LOAD_CONST               2 ('HG_internet_disable_rule_output')
             30 LOAD_FAST                0 (output)
             32 CONTAINS_OP              0
             34 POP_JUMP_IF_FALSE       47 (to 130)

208          36 LOAD_GLOBAL              3 (NULL + print)
             46 LOAD_CONST               3 ('[*] 偵測到全域舊規則：HG_internet_disable_rule_output')
             48 CALL                     1
             56 POP_TOP

209          58 LOAD_GLOBAL              1 (NULL + run_netsh)
             68 BUILD_LIST               0
             70 LOAD_CONST               4 (('delete', 'rule', 'name=HG_internet_disable_rule_output'))
             72 LIST_EXTEND              1
             74 CALL                     1
             82 POP_TOP

210          84 LOAD_GLOBAL              3 (NULL + print)
             94 LOAD_CONST               5 ('  [-] 已移除')
             96 CALL                     1
            104 POP_TOP

211         106 LOAD_GLOBAL              5 (NULL + log_action)
            116 LOAD_CONST               6 ('移除殘留全域舊規則 HG_internet_disable_rule_output')
            118 CALL                     1
            126 POP_TOP
            128 RETURN_CONST             0 (None)

207     >>  130 RETURN_CONST             0 (None)


# ====== add_block_rules ======
214           0 RESUME                   0

215           2 LOAD_GLOBAL              0 (APP_NAMES)
             12 GET_ITER
        >>   14 FOR_ITER               159 (to 336)
             18 STORE_FAST               5 (app)

216          20 LOAD_CONST               1 ('HG-')
             22 LOAD_FAST                0 (ip)
             24 FORMAT_VALUE             0
             26 LOAD_CONST               2 ('(')
             28 LOAD_FAST                1 (country)
             30 FORMAT_VALUE             0
             32 LOAD_CONST               3 (')-')
             34 LOAD_FAST                5 (app)
             36 FORMAT_VALUE             0
             38 LOAD_CONST               4 ('-IN')
             40 BUILD_STRING             7
             42 STORE_FAST               6 (name_in)

217          44 LOAD_CONST               1 ('HG-')
             46 LOAD_FAST                0 (ip)
             48 FORMAT_VALUE             0
             50 LOAD_CONST               2 ('(')
             52 LOAD_FAST                1 (country)
             54 FORMAT_VALUE             0
             56 LOAD_CONST               3 (')-')
             58 LOAD_FAST                5 (app)
             60 FORMAT_VALUE             0
             62 LOAD_CONST               5 ('-OUT')
             64 BUILD_STRING             7
             66 STORE_FAST               7 (name_out)

218          68 LOAD_FAST                2 (program_paths)
             70 LOAD_FAST                5 (app)
             72 BINARY_SUBSCR
             76 STORE_FAST               8 (prog)

220          78 LOAD_GLOBAL              3 (NULL + run_netsh)
             88 LOAD_CONST               6 ('add')
             90 LOAD_CONST               7 ('rule')
             92 LOAD_CONST               8 ('name=')
             94 LOAD_FAST                6 (name_in)
             96 FORMAT_VALUE             0
             98 BUILD_STRING             2

221         100 LOAD_CONST               9 ('dir=in')
            102 LOAD_CONST              10 ('remoteip=')
            104 LOAD_FAST                0 (ip)
            106 FORMAT_VALUE             0
            108 BUILD_STRING             2
            110 LOAD_CONST              11 ('action=block')

222         112 LOAD_CONST              12 ('program=')
            114 LOAD_FAST                8 (prog)
            116 FORMAT_VALUE             0
            118 BUILD_STRING             2
            120 LOAD_CONST              13 ('protocol=any')

220         122 BUILD_LIST               8
            124 CALL                     1
            132 POP_TOP

223         134 LOAD_FAST                3 (current)
            136 LOAD_CONST              14 (1)
            138 BINARY_OP               13 (+=)
            142 STORE_FAST               3 (current)

224         144 LOAD_FAST                4 (total)
            146 POP_JUMP_IF_FALSE       22 (to 192)

225         148 LOAD_GLOBAL              5 (NULL + progress_bar)
            158 LOAD_FAST                3 (current)
            160 LOAD_FAST                4 (total)
            162 LOAD_FAST                0 (ip)
            164 FORMAT_VALUE             0
            166 LOAD_CONST               2 ('(')
            168 LOAD_FAST                1 (country)
            170 FORMAT_VALUE             0
            172 LOAD_CONST              15 (') ')
            174 LOAD_FAST                5 (app)
            176 FORMAT_VALUE             0
            178 LOAD_CONST              16 (' IN')
            180 BUILD_STRING             6
            182 CALL                     3
            190 POP_TOP

227     >>  192 LOAD_GLOBAL              3 (NULL + run_netsh)
            202 LOAD_CONST               6 ('add')
            204 LOAD_CONST               7 ('rule')
            206 LOAD_CONST               8 ('name=')
            208 LOAD_FAST                7 (name_out)
            210 FORMAT_VALUE             0
            212 BUILD_STRING             2

228         214 LOAD_CONST              17 ('dir=out')
            216 LOAD_CONST              10 ('remoteip=')
            218 LOAD_FAST                0 (ip)
            220 FORMAT_VALUE             0
            222 BUILD_STRING             2
            224 LOAD_CONST              11 ('action=block')

229         226 LOAD_CONST              12 ('program=')
            228 LOAD_FAST                8 (prog)
            230 FORMAT_VALUE             0
            232 BUILD_STRING             2
            234 LOAD_CONST              13 ('protocol=any')

227         236 BUILD_LIST               8
            238 CALL                     1
            246 POP_TOP

230         248 LOAD_FAST                3 (current)
            250 LOAD_CONST              14 (1)
            252 BINARY_OP               13 (+=)
            256 STORE_FAST               3 (current)

231         258 LOAD_FAST                4 (total)
            260 POP_JUMP_IF_FALSE       22 (to 306)

232         262 LOAD_GLOBAL              5 (NULL + progress_bar)
            272 LOAD_FAST                3 (current)
            274 LOAD_FAST                4 (total)
            276 LOAD_FAST                0 (ip)
            278 FORMAT_VALUE             0
            280 LOAD_CONST               2 ('(')
            282 LOAD_FAST                1 (country)
            284 FORMAT_VALUE             0
            286 LOAD_CONST              15 (') ')
            288 LOAD_FAST                5 (app)
            290 FORMAT_VALUE             0
            292 LOAD_CONST              18 (' OUT')
            294 BUILD_STRING             6
            296 CALL                     3
            304 POP_TOP

234     >>  306 LOAD_GLOBAL              7 (NULL + log_action)
            316 LOAD_CONST              19 ('已新增 ')
            318 LOAD_FAST                6 (name_in)
            320 FORMAT_VALUE             0
            322 BUILD_STRING             2
            324 CALL                     1
            332 POP_TOP
            334 JUMP_BACKWARD          161 (to 14)

215     >>  336 END_FOR

235         338 LOAD_FAST                3 (current)
            340 RETURN_VALUE


# ====== remove_all_rules ======
238           0 RESUME                   0

240           2 LOAD_GLOBAL              1 (NULL + print)
             12 LOAD_CONST               1 ('[*] 正在清除 HG 防火牆規則…')
             14 CALL                     1
             22 POP_TOP

241          24 NOP

242          26 LOAD_CONST               2 ("@(Get-NetFirewallRule | Where-Object { $_.DisplayName -like 'HG-*' }).Count")
             28 STORE_FAST               0 (ps)

243          30 LOAD_GLOBAL              3 (NULL + subprocess)
             40 LOAD_ATTR                4 (run)
             60 LOAD_CONST               3 ('powershell')
             62 LOAD_CONST               4 ('-NoProfile')
             64 LOAD_CONST               5 ('-Command')
             66 LOAD_FAST                0 (ps)
             68 BUILD_LIST               4

244          70 LOAD_CONST               6 (True)
             72 LOAD_GLOBAL              2 (subprocess)
             82 LOAD_ATTR                6 (CREATE_NO_WINDOW)

243         102 KW_NAMES                 7 (('capture_output', 'creationflags'))
            104 CALL                     3
            112 STORE_FAST               1 (result)

245         114 LOAD_FAST                1 (result)
            116 LOAD_ATTR                8 (stdout)
            136 COPY                     1
            138 POP_JUMP_IF_TRUE         2 (to 144)
            140 POP_TOP
            142 LOAD_CONST               8 (b'')
        >>  144 LOAD_ATTR               11 (NULL|self + decode)
            164 LOAD_CONST               9 ('utf-8')
            166 LOAD_CONST              10 ('replace')
            168 KW_NAMES                11 (('errors',))
            170 CALL                     2
            178 LOAD_ATTR               13 (NULL|self + strip)
            198 CALL                     0
            206 STORE_FAST               2 (before)

249     >>  208 LOAD_CONST              13 ("Get-NetFirewallRule | Where-Object { $_.DisplayName -like 'HG-*' } | Remove-NetFirewallRule -Confirm:$false")
            210 STORE_FAST               3 (ps_del)

251         212 NOP

252         214 LOAD_GLOBAL              3 (NULL + subprocess)
            224 LOAD_ATTR                4 (run)
            244 LOAD_CONST               3 ('powershell')
            246 LOAD_CONST               4 ('-NoProfile')
            248 LOAD_CONST               5 ('-Command')
            250 LOAD_FAST                3 (ps_del)
            252 BUILD_LIST               4

253         254 LOAD_CONST               6 (True)
            256 LOAD_GLOBAL              2 (subprocess)
            266 LOAD_ATTR                6 (CREATE_NO_WINDOW)

252         286 KW_NAMES                 7 (('capture_output', 'creationflags'))
            288 CALL                     3
            296 POP_TOP

258     >>  298 NOP

259         300 LOAD_GLOBAL              3 (NULL + subprocess)
            310 LOAD_ATTR                4 (run)
            330 LOAD_CONST               3 ('powershell')
            332 LOAD_CONST               4 ('-NoProfile')
            334 LOAD_CONST               5 ('-Command')
            336 LOAD_FAST_CHECK          0 (ps)
            338 BUILD_LIST               4

260         340 LOAD_CONST               6 (True)
            342 LOAD_GLOBAL              2 (subprocess)
            352 LOAD_ATTR                6 (CREATE_NO_WINDOW)

259         372 KW_NAMES                 7 (('capture_output', 'creationflags'))
            374 CALL                     3
            382 STORE_FAST               4 (result2)

261         384 LOAD_FAST                4 (result2)
            386 LOAD_ATTR                8 (stdout)
            406 COPY                     1
            408 POP_JUMP_IF_TRUE         2 (to 414)
            410 POP_TOP
            412 LOAD_CONST               8 (b'')
        >>  414 LOAD_ATTR               11 (NULL|self + decode)
            434 LOAD_CONST               9 ('utf-8')
            436 LOAD_CONST              10 ('replace')
            438 KW_NAMES                11 (('errors',))
            440 CALL                     2
            448 LOAD_ATTR               13 (NULL|self + strip)
            468 CALL                     0
            476 STORE_FAST               5 (after)

265     >>  478 LOAD_FAST                2 (before)
            480 LOAD_CONST              14 ('0')
            482 COMPARE_OP              40 (==)
            486 POP_JUMP_IF_TRUE         2 (to 492)
            488 LOAD_FAST                2 (before)
            490 POP_JUMP_IF_TRUE        12 (to 516)

266     >>  492 LOAD_GLOBAL              1 (NULL + print)
            502 LOAD_CONST              15 ('  [-] 沒有找到 HG 規則')
            504 CALL                     1
            512 POP_TOP
            514 RETURN_CONST            22 (None)

268     >>  516 LOAD_GLOBAL             15 (NULL + log_action)
            526 LOAD_CONST              16 ('已清除 ')
            528 LOAD_FAST                2 (before)
            530 FORMAT_VALUE             0
            532 LOAD_CONST              17 (' 條 HG 規則')
            534 BUILD_STRING             3
            536 CALL                     1
            544 POP_TOP

269         546 LOAD_FAST                5 (after)
            548 POP_JUMP_IF_FALSE        2 (to 554)
            550 LOAD_FAST                5 (after)
            552 JUMP_FORWARD             1 (to 556)
        >>  554 LOAD_CONST              14 ('0')
        >>  556 STORE_FAST               6 (remaining)

270         558 LOAD_FAST                6 (remaining)
            560 LOAD_CONST              14 ('0')
            562 COMPARE_OP              55 (!=)
            566 POP_JUMP_IF_FALSE       16 (to 600)

271         568 LOAD_GLOBAL              1 (NULL + print)
            578 LOAD_CONST              18 ('  [i] 剩餘 ')
            580 LOAD_FAST                6 (remaining)
            582 FORMAT_VALUE             0
            584 LOAD_CONST              19 (' 條（可能為系統規則）')
            586 BUILD_STRING             3
            588 CALL                     1
            596 POP_TOP
            598 RETURN_CONST            22 (None)

273     >>  600 LOAD_GLOBAL              1 (NULL + print)
            610 LOAD_CONST              20 ('  [✓] 已清除 ')
            612 LOAD_FAST                2 (before)
            614 FORMAT_VALUE             0
            616 LOAD_CONST              21 (' 條規則')
            618 BUILD_STRING             3
            620 CALL                     1
            628 POP_TOP
            630 RETURN_CONST            22 (None)
        >>  632 PUSH_EXC_INFO

246         634 POP_TOP

247         636 LOAD_CONST              12 ('?')
            638 STORE_FAST               2 (before)
            640 POP_EXCEPT
            642 JUMP_BACKWARD          218 (to 208)
        >>  644 COPY                     3
            646 POP_EXCEPT
            648 RERAISE                  1
        >>  650 PUSH_EXC_INFO

254         652 POP_TOP

255         654 POP_EXCEPT
            656 JUMP_BACKWARD          180 (to 298)
        >>  658 COPY                     3
            660 POP_EXCEPT
            662 RERAISE                  1
        >>  664 PUSH_EXC_INFO

262         666 POP_TOP

263         668 LOAD_CONST              12 ('?')
            670 STORE_FAST               5 (after)
            672 POP_EXCEPT
            674 JUMP_BACKWARD           99 (to 478)
        >>  676 COPY                     3
            678 POP_EXCEPT
            680 RERAISE                  1
ExceptionTable:
  26 to 206 -> 632 [0]
  214 to 296 -> 650 [0]
  300 to 476 -> 664 [0]
  632 to 638 -> 644 [1] lasti
  650 to 652 -> 658 [1] lasti
  664 to 670 -> 676 [1] lasti


# ====== select_hn_root ======
              0 MAKE_CELL                8 (saved)

286           2 RESUME                   0

287           4 LOAD_GLOBAL              1 (NULL + load_config)
             14 CALL                     0
             22 STORE_FAST               0 (cfg)

288          24 LOAD_FAST                0 (cfg)
             26 LOAD_ATTR                3 (NULL|self + get)
             46 LOAD_CONST               1 ('hn_path')
             48 LOAD_CONST               2 ('')
             50 CALL                     2
             58 LOAD_ATTR                5 (NULL|self + replace)
             78 LOAD_CONST               3 ('/')
             80 LOAD_CONST               4 ('\\')
             82 CALL                     2
             90 STORE_DEREF              8 (saved)

289          92 LOAD_DEREF               8 (saved)
             94 POP_JUMP_IF_FALSE       70 (to 236)

290          96 LOAD_GLOBAL              7 (NULL + all)
            106 LOAD_CLOSURE             8 (saved)
            108 BUILD_TUPLE              1
            110 LOAD_CONST               5 (<code object <genexpr> at 0x000002670E9218F0, file "HG_Firewall.py", line 290>)
            112 MAKE_FUNCTION            8 (closure)
            114 LOAD_GLOBAL              8 (APP_NAMES)
            124 GET_ITER
            126 CALL                     0
            134 CALL                     1
            142 STORE_FAST               1 (valid)

291         144 LOAD_FAST                1 (valid)
            146 POP_JUMP_IF_FALSE       30 (to 208)

292         148 LOAD_GLOBAL             11 (NULL + print)
            158 LOAD_CONST               6 ('[*] 自動使用上次路徑：')
            160 LOAD_DEREF               8 (saved)
            162 FORMAT_VALUE             0
            164 BUILD_STRING             2
            166 CALL                     1
            174 POP_TOP

293         176 LOAD_GLOBAL             13 (NULL + log_info)
            186 LOAD_CONST               7 ('使用上次路徑: ')
            188 LOAD_DEREF               8 (saved)
            190 FORMAT_VALUE             0
            192 BUILD_STRING             2
            194 CALL                     1
            202 POP_TOP

294         204 LOAD_DEREF               8 (saved)
            206 RETURN_VALUE

296     >>  208 LOAD_GLOBAL             11 (NULL + print)
            218 LOAD_CONST               8 ('[!] 上次路徑已失效（找不到程式），請重新輸入')
            220 CALL                     1
            228 POP_TOP

297         230 LOAD_CONST               2 ('')
            232 STORE_FAST               2 (path)
            234 JUMP_FORWARD             2 (to 240)

299     >>  236 LOAD_CONST               2 ('')
            238 STORE_FAST               2 (path)

301     >>  240 LOAD_GLOBAL             11 (NULL + print)
            250 LOAD_CONST               9 ('[?] 請指定 HnG 遊戲安裝路徑')
            252 CALL                     1
            260 POP_TOP

302     >>  262 NOP

303     >>  264 LOAD_FAST                2 (path)
            266 POP_JUMP_IF_TRUE        86 (to 440)

304         268 LOAD_GLOBAL             15 (NULL + input)
            278 LOAD_CONST              10 ('路徑: ')
            280 CALL                     1
            288 LOAD_ATTR               17 (NULL|self + strip)
            308 CALL                     0
            316 LOAD_ATTR               17 (NULL|self + strip)
            336 LOAD_CONST              11 ('"')
            338 CALL                     1
            346 LOAD_ATTR               17 (NULL|self + strip)
            366 LOAD_CONST              12 ("'")
            368 CALL                     1
            376 LOAD_ATTR                5 (NULL|self + replace)
            396 LOAD_CONST               3 ('/')
            398 LOAD_CONST               4 ('\\')
            400 CALL                     2
            408 LOAD_ATTR               19 (NULL|self + rstrip)
            428 LOAD_CONST               4 ('\\')
            430 CALL                     1
            438 STORE_FAST               2 (path)

305     >>  440 LOAD_FAST                2 (path)
            442 POP_JUMP_IF_TRUE        14 (to 472)

306         444 LOAD_GLOBAL             11 (NULL + print)
            454 LOAD_CONST              13 ('[!] 路徑不得留空')
            456 CALL                     1
            464 POP_TOP

307         466 LOAD_CONST               2 ('')
            468 STORE_FAST               2 (path)

308         470 JUMP_BACKWARD          105 (to 262)

309     >>  472 BUILD_LIST               0
            474 STORE_FAST               3 (missing)

310         476 LOAD_GLOBAL              8 (APP_NAMES)
            486 GET_ITER
        >>  488 FOR_ITER                86 (to 664)
            492 STORE_FAST               4 (app)

311         494 LOAD_GLOBAL             20 (os)
            504 LOAD_ATTR               22 (path)
            524 LOAD_ATTR               25 (NULL|self + join)
            544 LOAD_FAST                2 (path)
            546 LOAD_FAST                4 (app)
            548 FORMAT_VALUE             0
            550 LOAD_CONST              14 ('.exe')
            552 BUILD_STRING             2
            554 CALL                     2
            562 STORE_FAST               5 (exe)

312         564 LOAD_GLOBAL             20 (os)
            574 LOAD_ATTR               22 (path)
            594 LOAD_ATTR               27 (NULL|self + isfile)
            614 LOAD_FAST                5 (exe)
            616 CALL                     1
            624 POP_JUMP_IF_FALSE        1 (to 628)
            626 JUMP_BACKWARD           70 (to 488)

313     >>  628 LOAD_FAST                3 (missing)
            630 LOAD_ATTR               29 (NULL|self + append)
            650 LOAD_FAST                4 (app)
            652 CALL                     1
            660 POP_TOP
            662 JUMP_BACKWARD           88 (to 488)

310     >>  664 END_FOR

314         666 LOAD_FAST                3 (missing)
            668 POP_JUMP_IF_FALSE      112 (to 894)

315         670 LOAD_GLOBAL             11 (NULL + print)
            680 LOAD_CONST              15 ('[!] 找不到以下檔案：')
            682 CALL                     1
            690 POP_TOP

316         692 LOAD_FAST                3 (missing)
            694 GET_ITER
        >>  696 FOR_ITER                17 (to 734)
            700 STORE_FAST               6 (m)

317         702 LOAD_GLOBAL             11 (NULL + print)
            712 LOAD_CONST              16 ('    - ')
            714 LOAD_FAST                6 (m)
            716 FORMAT_VALUE             0
            718 LOAD_CONST              14 ('.exe')
            720 BUILD_STRING             3
            722 CALL                     1
            730 POP_TOP
            732 JUMP_BACKWARD           19 (to 696)

316     >>  734 END_FOR

318         736 LOAD_GLOBAL             11 (NULL + print)
            746 LOAD_CONST              17 ('    請確認路徑後再試。\n')
            748 CALL                     1
            756 POP_TOP

319         758 LOAD_GLOBAL             15 (NULL + input)
            768 LOAD_CONST              18 ('按 Enter 重試，或輸入 Q 離開: ')
            770 CALL                     1
            778 LOAD_ATTR               17 (NULL|self + strip)
            798 CALL                     0
            806 LOAD_ATTR               31 (NULL|self + upper)
            826 CALL                     0
            834 STORE_FAST               7 (retry)

320         836 LOAD_FAST                7 (retry)
            838 LOAD_CONST              19 ('Q')
            840 COMPARE_OP              40 (==)
            844 POP_JUMP_IF_FALSE       21 (to 888)

321         846 LOAD_GLOBAL             33 (NULL + sys)
            856 LOAD_ATTR               34 (exit)
            876 LOAD_CONST              20 (0)
            878 CALL                     1
            886 POP_TOP

322     >>  888 LOAD_CONST               2 ('')
            890 STORE_FAST               2 (path)
            892 JUMP_FORWARD            82 (to 1058)

324     >>  894 LOAD_GLOBAL             11 (NULL + print)
            904 LOAD_CONST              21 ('\n[✓] 已確認以下程式：')
            906 CALL                     1
            914 POP_TOP

325         916 LOAD_GLOBAL              8 (APP_NAMES)
            926 GET_ITER
        >>  928 FOR_ITER                17 (to 966)
            932 STORE_FAST               4 (app)

326         934 LOAD_GLOBAL             11 (NULL + print)
            944 LOAD_CONST              22 ('    ')
            946 LOAD_FAST                4 (app)
            948 FORMAT_VALUE             0
            950 LOAD_CONST              14 ('.exe')
            952 BUILD_STRING             3
            954 CALL                     1
            962 POP_TOP
            964 JUMP_BACKWARD           19 (to 928)

325     >>  966 END_FOR

327         968 LOAD_GLOBAL             13 (NULL + log_info)
            978 LOAD_CONST              23 ('遊戲路徑: ')
            980 LOAD_FAST                2 (path)
            982 FORMAT_VALUE             0
            984 BUILD_STRING             2
            986 CALL                     1
            994 POP_TOP

328         996 LOAD_GLOBAL             37 (NULL + save_config)
           1006 LOAD_FAST                2 (path)
           1008 LOAD_FAST                0 (cfg)
           1010 LOAD_ATTR                3 (NULL|self + get)
           1030 LOAD_CONST              24 ('last_mode')
           1032 LOAD_CONST               2 ('')
           1034 CALL                     2
           1042 KW_NAMES                25 (('hn_path', 'last_mode'))
           1044 CALL                     2
           1052 POP_TOP

329        1054 LOAD_FAST                2 (path)
           1056 RETURN_VALUE

302     >> 1058 EXTENDED_ARG             1
           1060 JUMP_BACKWARD          399 (to 264)

Disassembly of <code object <genexpr> at 0x000002670E9218F0, file "HG_Firewall.py", line 290>:
              0 COPY_FREE_VARS           1

290           2 RETURN_GENERATOR
              4 POP_TOP
              6 RESUME                   0
              8 LOAD_FAST                0 (.0)
        >>   10 FOR_ITER                68 (to 150)
             14 STORE_FAST               1 (app)
             16 LOAD_GLOBAL              0 (os)
             26 LOAD_ATTR                2 (path)
             46 LOAD_ATTR                5 (NULL|self + isfile)
             66 LOAD_GLOBAL              0 (os)
             76 LOAD_ATTR                2 (path)
             96 LOAD_ATTR                7 (NULL|self + join)
            116 LOAD_DEREF               2 (saved)
            118 LOAD_FAST                1 (app)
            120 FORMAT_VALUE             0
            122 LOAD_CONST               0 ('.exe')
            124 BUILD_STRING             2
            126 CALL                     2
            134 CALL                     1
            142 YIELD_VALUE              1
            144 RESUME                   1
            146 POP_TOP
            148 JUMP_BACKWARD           70 (to 10)
        >>  150 END_FOR
            152 RETURN_CONST             1 (None)
        >>  154 CALL_INTRINSIC_1         3 (INTRINSIC_STOPITERATION_ERROR)
            156 RERAISE                  1
ExceptionTable:
  6 to 152 -> 154 [0] lasti


# ====== invoke_block ======
332           0 RESUME                   0

333           2 LOAD_GLOBAL              1 (NULL + print)
             12 LOAD_CONST               1 ('\n[+] ')
             14 LOAD_FAST                0 (label)
             16 FORMAT_VALUE             0
             18 LOAD_CONST               2 (' …')
             20 BUILD_STRING             3
             22 CALL                     1
             30 POP_TOP

335          32 LOAD_GLOBAL              3 (NULL + remove_all_rules)
             42 CALL                     0
             50 POP_TOP

336          52 LOAD_GLOBAL              5 (NULL + time)
             62 LOAD_ATTR                6 (sleep)
             82 LOAD_CONST               3 (0.5)
             84 CALL                     1
             92 POP_TOP

337          94 LOAD_GLOBAL              8 (ALL_IPS)
            104 GET_ITER
            106 LOAD_FAST_AND_CLEAR      2 (x)
            108 SWAP                     2
            110 BUILD_LIST               0
            112 SWAP                     2
        >>  114 FOR_ITER                13 (to 144)
            118 STORE_FAST               2 (x)
            120 PUSH_NULL
            122 LOAD_FAST                1 (filter_func)
            124 LOAD_FAST                2 (x)
            126 CALL                     1
            134 POP_JUMP_IF_TRUE         1 (to 138)
            136 JUMP_BACKWARD           12 (to 114)
        >>  138 LOAD_FAST                2 (x)
            140 LIST_APPEND              2
            142 JUMP_BACKWARD           15 (to 114)
        >>  144 END_FOR
            146 STORE_FAST               3 (block_list)
            148 STORE_FAST               2 (x)

338         150 LOAD_GLOBAL             11 (NULL + len)
            160 LOAD_FAST                3 (block_list)
            162 CALL                     1
            170 LOAD_GLOBAL             11 (NULL + len)
            180 LOAD_GLOBAL             12 (APP_NAMES)
            190 CALL                     1
            198 BINARY_OP                5 (*)
            202 LOAD_CONST               4 (2)
            204 BINARY_OP                5 (*)
            208 STORE_FAST               4 (total)

339         210 LOAD_GLOBAL              1 (NULL + print)
            220 LOAD_CONST               5 ('    共 ')
            222 LOAD_GLOBAL             11 (NULL + len)
            232 LOAD_FAST                3 (block_list)
            234 CALL                     1
            242 FORMAT_VALUE             0
            244 LOAD_CONST               6 (' 個 IP，將建立 ')
            246 LOAD_FAST                4 (total)
            248 FORMAT_VALUE             0
            250 LOAD_CONST               7 (' 條規則\n')
            252 BUILD_STRING             5
            254 CALL                     1
            262 POP_TOP

342         264 LOAD_CONST               8 (0)
            266 STORE_FAST               5 (current)

343         268 LOAD_FAST                3 (block_list)
            270 GET_ITER
        >>  272 FOR_ITER                27 (to 330)
            276 STORE_FAST               6 (item)

344         278 LOAD_GLOBAL             15 (NULL + add_block_rules)
            288 LOAD_FAST                6 (item)
            290 LOAD_CONST               9 ('ip')
            292 BINARY_SUBSCR
            296 LOAD_FAST                6 (item)
            298 LOAD_CONST              10 ('country')
            300 BINARY_SUBSCR
            304 LOAD_GLOBAL             16 (app_paths)
            314 LOAD_FAST                5 (current)
            316 LOAD_FAST                4 (total)
            318 CALL                     5
            326 STORE_FAST               5 (current)
            328 JUMP_BACKWARD           29 (to 272)

343     >>  330 END_FOR

345         332 LOAD_GLOBAL              1 (NULL + print)
            342 CALL                     0
            350 POP_TOP

346         352 LOAD_GLOBAL             19 (NULL + show_current_rules)
            362 CALL                     0
            370 POP_TOP

347         372 LOAD_GLOBAL              1 (NULL + print)
            382 LOAD_CONST              11 ('\n[✓] ')
            384 LOAD_GLOBAL             11 (NULL + len)
            394 LOAD_FAST                3 (block_list)
            396 CALL                     1
            404 FORMAT_VALUE             0
            406 LOAD_CONST              12 (' 個 IP 已雙向封鎖（傳入 + 傳出）')
            408 BUILD_STRING             3
            410 CALL                     1
            418 POP_TOP

348         420 LOAD_GLOBAL             21 (NULL + log_action)
            430 LOAD_FAST                0 (label)
            432 FORMAT_VALUE             0
            434 LOAD_CONST              13 ('：')
            436 LOAD_GLOBAL             11 (NULL + len)
            446 LOAD_FAST                3 (block_list)
            448 CALL                     1
            456 FORMAT_VALUE             0
            458 LOAD_CONST              14 (' 個 IP 已雙向封鎖')
            460 BUILD_STRING             4
            462 CALL                     1
            470 POP_TOP
            472 RETURN_CONST             0 (None)
        >>  474 SWAP                     2
            476 POP_TOP

337         478 SWAP                     2
            480 STORE_FAST               2 (x)
            482 RERAISE                  0
ExceptionTable:
  110 to 134 -> 474 [2]
  138 to 144 -> 474 [2]


# ====== write_banner ======
351           0 RESUME                   0

352           2 LOAD_GLOBAL              1 (NULL + os)
             12 LOAD_ATTR                2 (system)
             32 LOAD_CONST               1 ('cls')
             34 CALL                     1
             42 POP_TOP

353          44 LOAD_GLOBAL              5 (NULL + print)
             54 LOAD_CONST               2 ('╔═══════════════════════════════════════════╗')
             56 CALL                     1
             64 POP_TOP

354          66 LOAD_GLOBAL              5 (NULL + print)
             76 LOAD_CONST               3 ('║        HG 伺服器鎖定 v2.0                 ║')
             78 CALL                     1
             86 POP_TOP

355          88 LOAD_GLOBAL              5 (NULL + print)
             98 LOAD_CONST               4 ('║        雙向（傳入 + 傳出）封鎖            ║')
            100 CALL                     1
            108 POP_TOP

356         110 LOAD_GLOBAL              5 (NULL + print)
            120 LOAD_CONST               5 ('╚═══════════════════════════════════════════╝')
            122 CALL                     1
            130 POP_TOP

357         132 LOAD_GLOBAL              5 (NULL + print)
            142 LOAD_CONST               6 ('目標程式：hngsync.exe、HeroesAndGeneralsDesktop.exe')
            144 CALL                     1
            152 POP_TOP

358         154 LOAD_GLOBAL              5 (NULL + print)
            164 LOAD_CONST               7 ('封鎖模式：傳入 / 傳出雙向封鎖，全協議，全埠')
            166 CALL                     1
            174 POP_TOP

359         176 LOAD_GLOBAL              5 (NULL + print)
            186 CALL                     0
            194 POP_TOP

360         196 LOAD_GLOBAL              5 (NULL + print)
            206 LOAD_CONST               8 ('規則計算說明：')
            208 CALL                     1
            216 POP_TOP

361         218 LOAD_GLOBAL              5 (NULL + print)
            228 LOAD_CONST               9 ('  每個 IP × 2 個程式 × 2 方向 = 每 IP 4 條規則')
            230 CALL                     1
            238 POP_TOP

362         240 LOAD_GLOBAL              5 (NULL + print)
            250 CALL                     0
            258 POP_TOP

363         260 LOAD_GLOBAL              5 (NULL + print)
            270 LOAD_CONST              10 ('  各選項將產生的規則數量：')
            272 CALL                     1
            280 POP_TOP

364         282 LOAD_GLOBAL              5 (NULL + print)
            292 LOAD_CONST              11 ('    [1] AS-EU Only → 封鎖 3 個非亞歐 IP → 3×4 =  12 條規則')
            294 CALL                     1
            302 POP_TOP

365         304 LOAD_GLOBAL              5 (NULL + print)
            314 LOAD_CONST              12 ('    [2] EU Only   → 封鎖 5 個非歐洲 IP → 5×4 =  20 條規則')
            316 CALL                     1
            324 POP_TOP

366         326 LOAD_GLOBAL              5 (NULL + print)
            336 LOAD_CONST              13 ('    [3] AS Only   → 封鎖 11 個非亞洲 IP → 11×4 = 44 條規則')
            338 CALL                     1
            346 POP_TOP

367         348 LOAD_GLOBAL              5 (NULL + print)
            358 LOAD_CONST              14 ('    [4] HK Only   → 封鎖 12 個非香港 IP → 12×4 = 48 條規則')
            360 CALL                     1
            368 POP_TOP

368         370 LOAD_GLOBAL              5 (NULL + print)
            380 LOAD_CONST              15 ('    [5] Clear     → 清除所有規則 → 0 條')
            382 CALL                     1
            390 POP_TOP

369         392 LOAD_GLOBAL              5 (NULL + print)
            402 CALL                     0
            410 POP_TOP
            412 RETURN_CONST             0 (None)


# ====== main ======
372           0 RESUME                   0

376           2 LOAD_GLOBAL              1 (NULL + log_init)
             12 CALL                     0
             20 POP_TOP

377          22 LOAD_GLOBAL              3 (NULL + log_info)
             32 LOAD_CONST               1 ('使用者授權管理員權限')
             34 CALL                     1
             42 POP_TOP

380          44 LOAD_GLOBAL              5 (NULL + is_admin)
             54 CALL                     0
             62 POP_JUMP_IF_TRUE        22 (to 108)

381          64 LOAD_GLOBAL              7 (NULL + print)
             74 LOAD_CONST               2 ('[!] 需要管理員權限，正在請求…')
             76 CALL                     1
             84 POP_TOP

382          86 LOAD_GLOBAL              9 (NULL + run_as_admin)
             96 CALL                     0
            104 POP_TOP

383         106 RETURN_CONST             0 (None)

385     >>  108 LOAD_GLOBAL             11 (NULL + set_console_size)
            118 CALL                     0
            126 POP_TOP

387         128 LOAD_GLOBAL             13 (NULL + remove_old_v1_rules)
            138 CALL                     0
            146 POP_TOP

388         148 LOAD_GLOBAL              7 (NULL + print)
            158 CALL                     0
            166 POP_TOP

389         168 LOAD_GLOBAL             15 (NULL + remove_legacy_global_rule)
            178 CALL                     0
            186 POP_TOP

390         188 LOAD_GLOBAL              7 (NULL + print)
            198 CALL                     0
            206 POP_TOP

392         208 LOAD_GLOBAL             17 (NULL + write_banner)
            218 CALL                     0
            226 POP_TOP

393         228 LOAD_GLOBAL             19 (NULL + load_config)
            238 CALL                     0
            246 STORE_FAST               0 (cfg)

394         248 LOAD_GLOBAL             21 (NULL + select_hn_root)
            258 CALL                     0
            266 STORE_FAST               1 (hn_path)

396         268 BUILD_MAP                0
            270 STORE_GLOBAL            11 (app_paths)

397         272 LOAD_GLOBAL             24 (APP_NAMES)
            282 GET_ITER
        >>  284 FOR_ITER                44 (to 376)
            288 STORE_FAST               2 (app)

398         290 LOAD_GLOBAL             26 (os)
            300 LOAD_ATTR               28 (path)
            320 LOAD_ATTR               31 (NULL|self + join)
            340 LOAD_FAST                1 (hn_path)
            342 LOAD_FAST                2 (app)
            344 FORMAT_VALUE             0
            346 LOAD_CONST               3 ('.exe')
            348 BUILD_STRING             2
            350 CALL                     2
            358 LOAD_GLOBAL             22 (app_paths)
            368 LOAD_FAST                2 (app)
            370 STORE_SUBSCR
            374 JUMP_BACKWARD           46 (to 284)

397     >>  376 END_FOR

400         378 NOP

401     >>  380 LOAD_GLOBAL             19 (NULL + load_config)
            390 CALL                     0
            398 STORE_FAST               0 (cfg)

402         400 LOAD_FAST                0 (cfg)
            402 LOAD_ATTR               33 (NULL|self + get)
            422 LOAD_CONST               4 ('last_mode')
            424 LOAD_CONST               5 ('')
            426 CALL                     2
            434 STORE_FAST               3 (saved_mode)

403         436 LOAD_FAST                3 (saved_mode)
            438 POP_JUMP_IF_FALSE        6 (to 452)
            440 LOAD_CONST               6 ('  （目前設定：')
            442 LOAD_FAST                3 (saved_mode)
            444 FORMAT_VALUE             0
            446 LOAD_CONST               7 ('）')
            448 BUILD_STRING             3
            450 JUMP_FORWARD             1 (to 454)
        >>  452 LOAD_CONST               5 ('')
        >>  454 STORE_FAST               4 (mode_hint)

404         456 LOAD_GLOBAL              7 (NULL + print)
            466 CALL                     0
            474 POP_TOP

405         476 LOAD_GLOBAL              7 (NULL + print)
            486 LOAD_CONST               8 ('IP 分佈：')
            488 CALL                     1
            496 POP_TOP

406         498 LOAD_GLOBAL              7 (NULL + print)
            508 LOAD_CONST               9 ('  歐洲（EU）      法國×6  德國×1  波蘭×1')
            510 CALL                     1
            518 POP_TOP

407         520 LOAD_GLOBAL              7 (NULL + print)
            530 LOAD_CONST              10 ('  亞洲（AS）      新加坡×1  香港×1')
            532 CALL                     1
            540 POP_TOP

408         542 LOAD_GLOBAL              7 (NULL + print)
            552 LOAD_CONST              11 ('  北美（NA）      加拿大×1  美國×1')
            554 CALL                     1
            562 POP_TOP

409         564 LOAD_GLOBAL              7 (NULL + print)
            574 LOAD_CONST              12 ('  大洋洲（OC）    澳洲×1')
            576 CALL                     1
            584 POP_TOP

410         586 LOAD_GLOBAL              7 (NULL + print)
            596 CALL                     0
            604 POP_TOP

411         606 LOAD_GLOBAL              7 (NULL + print)
            616 LOAD_CONST              13 ('操作：')
            618 LOAD_FAST                4 (mode_hint)
            620 FORMAT_VALUE             0
            622 BUILD_STRING             2
            624 CALL                     1
            632 POP_TOP

412         634 LOAD_GLOBAL              7 (NULL + print)
            644 LOAD_CONST              14 ('  [1] AS-EU Only   只留亞洲 + 歐洲，封鎖北美 + 大洋洲')
            646 CALL                     1
            654 POP_TOP

413         656 LOAD_GLOBAL              7 (NULL + print)
            666 LOAD_CONST              15 ('  [2] EU Only     封鎖歐洲以外所有 IP')
            668 CALL                     1
            676 POP_TOP

414         678 LOAD_GLOBAL              7 (NULL + print)
            688 LOAD_CONST              16 ('  [3] AS Only     封鎖亞洲以外所有 IP')
            690 CALL                     1
            698 POP_TOP

415         700 LOAD_GLOBAL              7 (NULL + print)
            710 LOAD_CONST              17 ('  [4] HK Only     僅連接香港，封鎖其餘所有 IP')
            712 CALL                     1
            720 POP_TOP

416         722 LOAD_GLOBAL              7 (NULL + print)
            732 LOAD_CONST              18 ('  [5] Clear       移除所有 HG 防火牆規則')
            734 CALL                     1
            742 POP_TOP

417         744 LOAD_GLOBAL              7 (NULL + print)
            754 LOAD_CONST              19 ('  [6] 變更路徑    重新指定 HnG 資料夾')
            756 CALL                     1
            764 POP_TOP

418         766 LOAD_GLOBAL              7 (NULL + print)
            776 LOAD_CONST              20 ('  [0] 離開')
            778 CALL                     1
            786 POP_TOP

420         788 LOAD_GLOBAL             35 (NULL + input)
            798 LOAD_CONST              21 ('\n請選擇 (0-6): ')
            800 CALL                     1
            808 LOAD_ATTR               37 (NULL|self + strip)
            828 CALL                     0
            836 STORE_FAST               5 (choice)

422         838 LOAD_FAST                5 (choice)
            840 LOAD_CONST              22 ('1')
            842 COMPARE_OP              40 (==)
            846 POP_JUMP_IF_FALSE       28 (to 904)

423         848 LOAD_GLOBAL             39 (NULL + invoke_block)
            858 LOAD_CONST              23 ('僅連亞歐')
            860 LOAD_CONST              24 (<code object <lambda> at 0x000002670EC2E3F0, file "HG_Firewall.py", line 423>)
            862 MAKE_FUNCTION            0
            864 CALL                     2
            872 POP_TOP

424         874 LOAD_GLOBAL             41 (NULL + save_config)
            884 LOAD_FAST                1 (hn_path)
            886 LOAD_CONST              25 ('AS-EU Only')
            888 KW_NAMES                26 (('hn_path', 'last_mode'))
            890 CALL                     2
            898 POP_TOP
            900 EXTENDED_ARG             1
            902 JUMP_FORWARD           346 (to 1596)

425     >>  904 LOAD_FAST                5 (choice)
            906 LOAD_CONST              27 ('2')
            908 COMPARE_OP              40 (==)
            912 POP_JUMP_IF_FALSE       28 (to 970)

426         914 LOAD_GLOBAL             39 (NULL + invoke_block)
            924 LOAD_CONST              28 ('僅連歐洲')
            926 LOAD_CONST              29 (<code object <lambda> at 0x000002670EBBEB10, file "HG_Firewall.py", line 426>)
            928 MAKE_FUNCTION            0
            930 CALL                     2
            938 POP_TOP

427         940 LOAD_GLOBAL             41 (NULL + save_config)
            950 LOAD_FAST                1 (hn_path)
            952 LOAD_CONST              30 ('EU Only')
            954 KW_NAMES                26 (('hn_path', 'last_mode'))
            956 CALL                     2
            964 POP_TOP
            966 EXTENDED_ARG             1
            968 JUMP_FORWARD           313 (to 1596)

428     >>  970 LOAD_FAST                5 (choice)
            972 LOAD_CONST              31 ('3')
            974 COMPARE_OP              40 (==)
            978 POP_JUMP_IF_FALSE       28 (to 1036)

429         980 LOAD_GLOBAL             39 (NULL + invoke_block)
            990 LOAD_CONST              32 ('僅連亞洲')
            992 LOAD_CONST              33 (<code object <lambda> at 0x000002670EBBEBF0, file "HG_Firewall.py", line 429>)
            994 MAKE_FUNCTION            0
            996 CALL                     2
           1004 POP_TOP

430        1006 LOAD_GLOBAL             41 (NULL + save_config)
           1016 LOAD_FAST                1 (hn_path)
           1018 LOAD_CONST              34 ('AS Only')
           1020 KW_NAMES                26 (('hn_path', 'last_mode'))
           1022 CALL                     2
           1030 POP_TOP
           1032 EXTENDED_ARG             1
           1034 JUMP_FORWARD           280 (to 1596)

431     >> 1036 LOAD_FAST                5 (choice)
           1038 LOAD_CONST              35 ('4')
           1040 COMPARE_OP              40 (==)
           1044 POP_JUMP_IF_FALSE       27 (to 1100)

432        1046 LOAD_GLOBAL             39 (NULL + invoke_block)
           1056 LOAD_CONST              36 ('僅連香港')
           1058 LOAD_CONST              37 (<code object <lambda> at 0x000002670EBBF750, file "HG_Firewall.py", line 432>)
           1060 MAKE_FUNCTION            0
           1062 CALL                     2
           1070 POP_TOP

433        1072 LOAD_GLOBAL             41 (NULL + save_config)
           1082 LOAD_FAST                1 (hn_path)
           1084 LOAD_CONST              38 ('HK Only')
           1086 KW_NAMES                26 (('hn_path', 'last_mode'))
           1088 CALL                     2
           1096 POP_TOP
           1098 JUMP_FORWARD           248 (to 1596)

434     >> 1100 LOAD_FAST                5 (choice)
           1102 LOAD_CONST              39 ('5')
           1104 COMPARE_OP              40 (==)
           1108 POP_JUMP_IF_FALSE       77 (to 1264)

435        1110 LOAD_GLOBAL              7 (NULL + print)
           1120 LOAD_CONST              40 ('\n[+] 正在移除防火牆規則…')
           1122 CALL                     1
           1130 POP_TOP

436        1132 LOAD_GLOBAL             43 (NULL + remove_all_rules)
           1142 CALL                     0
           1150 POP_TOP

437        1152 LOAD_GLOBAL              7 (NULL + print)
           1162 CALL                     0
           1170 POP_TOP

438        1172 LOAD_GLOBAL             45 (NULL + show_current_rules)
           1182 CALL                     0
           1190 POP_TOP

439        1192 LOAD_GLOBAL              7 (NULL + print)
           1202 LOAD_CONST              41 ('\n[✓] 完成')
           1204 CALL                     1
           1212 POP_TOP

440        1214 LOAD_GLOBAL             47 (NULL + log_action)
           1224 LOAD_CONST              42 ('已執行 Clear，所有 HG 規則已清除')
           1226 CALL                     1
           1234 POP_TOP

441        1236 LOAD_GLOBAL             41 (NULL + save_config)
           1246 LOAD_FAST                1 (hn_path)
           1248 LOAD_CONST              43 ('無')
           1250 KW_NAMES                26 (('hn_path', 'last_mode'))
           1252 CALL                     2
           1260 POP_TOP
           1262 JUMP_FORWARD           166 (to 1596)

442     >> 1264 LOAD_FAST                5 (choice)
           1266 LOAD_CONST              44 ('6')
           1268 COMPARE_OP              40 (==)
           1272 POP_JUMP_IF_FALSE      122 (to 1518)

443        1274 LOAD_GLOBAL              7 (NULL + print)
           1284 CALL                     0
           1292 POP_TOP

444        1294 LOAD_GLOBAL             21 (NULL + select_hn_root)
           1304 CALL                     0
           1312 STORE_FAST               1 (hn_path)

445        1314 LOAD_GLOBAL             24 (APP_NAMES)
           1324 GET_ITER
        >> 1326 FOR_ITER                44 (to 1418)
           1330 STORE_FAST               2 (app)

446        1332 LOAD_GLOBAL             26 (os)
           1342 LOAD_ATTR               28 (path)
           1362 LOAD_ATTR               31 (NULL|self + join)
           1382 LOAD_FAST                1 (hn_path)
           1384 LOAD_FAST                2 (app)
           1386 FORMAT_VALUE             0
           1388 LOAD_CONST               3 ('.exe')
           1390 BUILD_STRING             2
           1392 CALL                     2
           1400 LOAD_GLOBAL             22 (app_paths)
           1410 LOAD_FAST                2 (app)
           1412 STORE_SUBSCR
           1416 JUMP_BACKWARD           46 (to 1326)

445     >> 1418 END_FOR

447        1420 LOAD_GLOBAL             41 (NULL + save_config)
           1430 LOAD_FAST                1 (hn_path)
           1432 LOAD_GLOBAL             19 (NULL + load_config)
           1442 CALL                     0
           1450 LOAD_ATTR               33 (NULL|self + get)
           1470 LOAD_CONST               4 ('last_mode')
           1472 LOAD_CONST               5 ('')
           1474 CALL                     2
           1482 KW_NAMES                26 (('hn_path', 'last_mode'))
           1484 CALL                     2
           1492 POP_TOP

448        1494 LOAD_GLOBAL              7 (NULL + print)
           1504 LOAD_CONST              45 ('[✓] 路徑已更新')
           1506 CALL                     1
           1514 POP_TOP
           1516 JUMP_FORWARD            39 (to 1596)

449     >> 1518 LOAD_FAST                5 (choice)
           1520 LOAD_CONST              46 ('0')
           1522 COMPARE_OP              40 (==)
           1526 POP_JUMP_IF_FALSE       12 (to 1552)

450        1528 LOAD_GLOBAL              7 (NULL + print)
           1538 LOAD_CONST              47 ('\n[-] 再見')
           1540 CALL                     1
           1548 POP_TOP

451        1550 RETURN_CONST             0 (None)

453     >> 1552 LOAD_GLOBAL              7 (NULL + print)
           1562 LOAD_CONST              48 ('\n[!] 無效選項')
           1564 CALL                     1
           1572 POP_TOP

454        1574 LOAD_GLOBAL             35 (NULL + input)
           1584 LOAD_CONST              49 ('按 Enter 繼續...')
           1586 CALL                     1
           1594 POP_TOP

456     >> 1596 LOAD_GLOBAL             17 (NULL + write_banner)
           1606 CALL                     0
           1614 POP_TOP

400        1616 EXTENDED_ARG             2
           1618 JUMP_BACKWARD          620 (to 380)

Disassembly of <code object <lambda> at 0x000002670EC2E3F0, file "HG_Firewall.py", line 423>:
423           0 RESUME                   0
              2 LOAD_FAST                0 (x)
              4 LOAD_CONST               1 ('region')
              6 BINARY_SUBSCR
             10 LOAD_CONST               2 (('NA', 'OC'))
             12 CONTAINS_OP              0
             14 RETURN_VALUE

Disassembly of <code object <lambda> at 0x000002670EBBEB10, file "HG_Firewall.py", line 426>:
426           0 RESUME                   0
              2 LOAD_FAST                0 (x)
              4 LOAD_CONST               1 ('region')
              6 BINARY_SUBSCR
             10 LOAD_CONST               2 ('EU')
             12 COMPARE_OP              55 (!=)
             16 RETURN_VALUE

Disassembly of <code object <lambda> at 0x000002670EBBEBF0, file "HG_Firewall.py", line 429>:
429           0 RESUME                   0
              2 LOAD_FAST                0 (x)
              4 LOAD_CONST               1 ('region')
              6 BINARY_SUBSCR
             10 LOAD_CONST               2 ('AS')
             12 COMPARE_OP              55 (!=)
             16 RETURN_VALUE

Disassembly of <code object <lambda> at 0x000002670EBBF750, file "HG_Firewall.py", line 432>:
432           0 RESUME                   0
              2 LOAD_FAST                0 (x)
              4 LOAD_CONST               1 ('ip')
              6 BINARY_SUBSCR
             10 LOAD_CONST               2 ('135.136.10.86')
             12 COMPARE_OP              55 (!=)
             16 RETURN_VALUE

