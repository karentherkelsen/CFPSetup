from opentrons import protocol_api
from math import ceil
import pandas as pd

metadata = {
    'apiLevel': '2.8',
    'protocolName': 'Cell-free expression buffer optimization setup',
    'description': '''This protocol is designed to set up a range of different 
    buffer compositions to optimize the buffer solution for cell-free expression.
    It involves adding Mg-glutamate, K-glutamate, and PEG-8000 to a premix 
    solution. A total of 343 combinations can be tested.''',
    'author': 'Karen Therkelsen (s173684@dtu.dk)',
}

################################################################################
#                                  User inputs                                 #
################################################################################

# Final concentrations of factors
Mg_final_conc = [3,5,7,9,11,13,15]
K_final_conc = [60,75,90,105,120,135,150]
P_final_conc = [0,1,2,3,4,5,6]

# Stock solution concentration
Mg_stock_conc = int(1000)   # mM
K_stock_conc = int(2000)    # mM
P_stock_conc = int(40)      # %

ff_dict = {
'Mg-glutamate': {306: 13.0, 340: 11.0, 291: 11.0, 102: 11.0, 289: 7.0, 267: 5.0, 125: 15.0, 11: 11.0, 146: 15.0, 229: 13.0, 165: 11.0, 263: 11.0, 287: 3.0, 159: 13.0, 95: 11.0, 67: 11.0, 4: 11.0, 247: 7.0, 65: 7.0, 85: 5.0, 222: 13.0, 211: 5.0, 330: 5.0, 292: 13.0, 91: 3.0, 6: 15.0, 217: 3.0, 169: 5.0, 331: 7.0, 90: 15.0, 117: 13.0, 106: 5.0, 256: 11.0, 138: 13.0, 107: 7.0, 174: 15.0, 132: 15.0, 18: 11.0, 315: 3.0, 92: 5.0, 80: 9.0, 127: 5.0, 123: 11.0, 251: 15.0, 294: 3.0, 236: 13.0, 131: 13.0, 322: 3.0, 197: 5.0, 111: 15.0, 154: 3.0, 189: 3.0, 122: 9.0, 120: 5.0, 328: 15.0, 208: 13.0, 301: 3.0, 73: 9.0, 59: 9.0, 12: 13.0, 273: 3.0, 27: 15.0, 332: 9.0, 342: 15.0, 89: 13.0, 29: 5.0, 58: 7.0, 212: 7.0, 93: 7.0, 150: 9.0, 105: 3.0, 112: 3.0, 162: 5.0, 327: 13.0, 305: 11.0, 283: 9.0, 179: 11.0, 119: 3.0, 14: 3.0, 245: 3.0, 191: 7.0, 261: 7.0, 51: 7.0, 9: 7.0, 242: 11.0, 16: 7.0, 188: 15.0, 0: 3.0, 249: 11.0, 187: 13.0, 62: 15.0, 171: 9.0, 278: 13.0, 234: 9.0, 70: 3.0, 177: 7.0, 204: 5.0, 41: 15.0, 244: 15.0, 206: 9.0, 231: 3.0, 329: 3.0, 161: 3.0, 39: 11.0, 288: 5.0, 78: 5.0, 232: 5.0, 192: 9.0, 324: 7.0, 17: 9.0, 257: 13.0, 224: 3.0, 88: 11.0, 167: 15.0, 272: 15.0, 42: 3.0, 334: 13.0, 172: 11.0, 139: 15.0, 163: 7.0, 186: 11.0, 5: 13.0, 225: 5.0, 175: 3.0, 38: 9.0, 233: 7.0, 180: 13.0, 158: 11.0, 341: 13.0, 147: 3.0, 100: 7.0, 34: 15.0, 110: 13.0, 218: 5.0, 321: 15.0, 19: 13.0, 213: 9.0, 44: 7.0, 314: 15.0, 207: 11.0, 185: 9.0, 108: 9.0, 299: 13.0, 79: 7.0, 325: 9.0, 201: 13.0, 8: 5.0, 285: 13.0, 99: 5.0, 300: 15.0, 293: 15.0, 275: 7.0, 28: 3.0, 31: 9.0, 55: 15.0, 32: 11.0, 219: 7.0, 48: 15.0, 284: 11.0, 227: 9.0, 33: 13.0, 35: 3.0, 260: 5.0, 63: 3.0, 157: 9.0, 128: 7.0, 46: 11.0, 66: 9.0, 274: 5.0, 173: 13.0, 326: 11.0, 336: 3.0, 277: 11.0, 269: 9.0, 168: 3.0, 47: 13.0, 113: 5.0, 268: 7.0, 40: 13.0, 21: 3.0, 101: 9.0, 164: 9.0, 69: 15.0, 53: 11.0, 137: 11.0, 24: 9.0, 304: 9.0, 184: 7.0, 134: 5.0, 270: 11.0, 116: 11.0, 205: 7.0, 142: 7.0, 295: 5.0, 199: 9.0, 316: 5.0, 56: 3.0, 61: 13.0, 271: 13.0, 221: 11.0, 223: 15.0, 84: 3.0, 181: 15.0, 228: 11.0, 114: 7.0, 311: 9.0, 290: 9.0, 323: 5.0, 118: 15.0, 258: 15.0, 170: 7.0, 145: 13.0, 337: 5.0, 298: 11.0, 54: 13.0, 176: 5.0, 307: 15.0, 194: 13.0, 198: 7.0, 214: 11.0, 230: 15.0, 248: 9.0, 182: 3.0, 246: 5.0, 98: 3.0, 339: 9.0, 238: 3.0, 130: 11.0, 97: 15.0, 310: 7.0, 82: 13.0, 250: 13.0, 60: 11.0, 94: 9.0, 193: 11.0, 140: 3.0, 160: 15.0, 148: 5.0, 220: 9.0, 202: 15.0, 152: 13.0, 309: 5.0, 135: 7.0, 81: 11.0, 124: 13.0, 23: 7.0, 10:9.0, 13: 15.0, 96: 13.0, 210: 3.0, 240: 7.0, 57: 5.0, 296: 7.0, 45: 9.0, 319: 11.0, 103: 13.0, 36: 5.0, 308: 3.0, 20: 15.0, 303: 7.0, 75: 13.0, 200: 11.0, 77: 3.0, 338: 7.0, 149: 7.0, 302: 5.0, 2: 7.0, 52: 9.0, 262: 9.0, 253: 5.0, 259: 3.0, 183: 5.0, 151: 11.0, 312: 11.0, 190: 5.0, 74: 11.0, 243: 13.0, 87: 9.0, 239: 5.0, 143: 9.0, 286: 15.0, 266: 3.0, 136: 9.0, 166: 13.0, 83: 15.0, 155: 5.0, 279: 15.0, 126: 3.0, 195: 15.0, 265: 15.0, 318: 9.0, 104: 15.0, 153: 15.0, 282: 7.0,226: 7.0, 25: 11.0, 196: 3.0, 64: 5.0, 15: 5.0, 297: 9.0, 109: 11.0, 26: 13.0, 76: 15.0, 43: 5.0, 280: 3.0, 3: 9.0, 49: 3.0, 333: 11.0, 30: 7.0, 121: 7.0, 115: 9.0, 320: 13.0, 216: 15.0, 264: 13.0, 209: 15.0, 1: 5.0, 313: 13.0, 22: 5.0, 317: 7.0, 7: 3.0, 141: 5.0, 86: 7.0, 241: 9.0, 215: 13.0, 68: 13.0, 50: 5.0, 156: 7.0, 252: 3.0, 254: 7.0, 276: 9.0, 178: 9.0, 281: 5.0, 237: 15.0, 71: 5.0, 129: 9.0, 144: 11.0, 335: 15.0, 133: 3.0, 203: 3.0, 255: 9.0, 72: 7.0, 235: 11.0, 37:7.0}, 
'K-glutamate': {306: 75.0, 340: 150.0, 291: 150.0, 102: 60.0, 289: 150.0, 267: 105.0, 125: 105.0, 11: 75.0, 146: 150.0, 229: 120.0, 165: 90.0, 263: 90.0, 287: 150.0, 159: 75.0, 95: 150.0, 67: 90.0, 4: 60.0, 247: 60.0, 65: 90.0, 85: 135.0, 222: 105.0, 211: 90.0, 330: 135.0, 292: 150.0, 91: 150.0, 6: 60.0, 217: 105.0, 169: 105.0, 331: 135.0, 90: 135.0, 117: 90.0, 106: 75.0, 256: 75.0, 138: 135.0, 107: 75.0, 174: 105.0, 132: 120.0, 18: 90.0, 315: 105.0, 92: 150.0, 80: 120.0, 127: 120.0, 123: 105.0, 251: 60.0, 294: 60.0, 236: 135.0, 131: 120.0, 322: 120.0, 197: 60.0, 111: 75.0, 154: 75.0, 189: 150.0, 122: 105.0, 120: 105.0, 328: 120.0, 208: 75.0, 301: 75.0, 73: 105.0, 59: 75.0, 12: 75.0, 273: 120.0, 27: 105.0, 332: 135.0, 342: 150.0, 89: 135.0, 29: 120.0, 58: 75.0, 212: 90.0, 93: 150.0, 150: 60.0, 105: 75.0, 112: 90.0, 162: 90.0, 327: 120.0, 305: 75.0, 283: 135.0, 179: 120.0, 119: 105.0, 14: 90.0, 245: 60.0, 191: 150.0, 261: 90.0, 51: 60.0, 9:75.0, 242: 150.0, 16: 90.0, 188: 135.0, 0: 60.0, 249: 60.0, 187: 135.0, 62: 75.0, 171: 105.0, 278: 120.0, 234: 135.0, 70: 105.0, 177: 120.0, 204: 75.0, 41: 135.0, 244: 150.0, 206: 75.0, 231: 135.0, 329: 135.0, 161: 90.0, 39: 135.0, 288: 150.0, 78: 120.0, 232: 135.0, 192: 150.0, 324: 120.0, 17: 90.0, 257: 75.0, 224: 120.0, 88: 135.0, 167: 90.0, 272: 105.0, 42: 150.0, 334: 135.0, 172: 105.0, 139: 135.0, 163: 90.0, 186: 135.0, 5: 60.0, 225: 120.0, 175: 120.0, 38: 135.0, 233: 135.0, 180: 120.0, 158: 75.0, 341: 150.0, 147: 60.0, 100: 60.0, 34: 120.0, 110: 75.0, 218: 105.0, 321: 105.0, 19: 90.0, 213: 90.0, 44: 150.0, 314: 90.0, 207: 75.0, 185: 135.0, 108: 75.0, 299: 60.0, 79: 120.0, 325: 120.0, 201: 60.0, 8: 75.0, 285: 135.0, 99: 60.0, 300: 60.0, 293: 150.0, 275: 120.0, 28: 120.0, 31: 120.0, 55: 60.0, 32: 120.0, 219: 105.0, 48: 150.0, 284: 135.0, 227: 120.0, 33: 120.0, 35: 135.0, 260: 90.0, 63: 90.0, 157: 75.0, 128: 120.0, 46: 150.0, 66: 90.0, 274: 120.0, 173: 105.0, 326: 120.0, 336: 150.0, 277: 120.0, 269: 105.0, 168: 105.0, 47: 150.0, 113: 90.0, 268: 105.0, 40: 135.0, 21: 105.0, 101: 60.0, 164: 90.0, 69: 90.0, 53: 60.0, 137: 135.0, 24: 105.0, 304: 75.0, 184: 135.0, 134: 135.0, 270: 105.0, 116: 90.0, 205: 75.0, 142: 150.0, 295: 60.0, 199: 60.0, 316: 105.0, 56: 75.0, 61: 75.0, 271: 105.0, 221: 105.0, 223: 105.0, 84: 135.0, 181: 120.0, 228: 120.0, 114: 90.0, 311: 90.0, 290: 150.0, 323: 120.0, 118: 90.0, 258: 75.0, 170: 105.0, 145: 150.0, 337: 150.0, 298: 60.0, 54: 60.0, 176: 120.0, 307: 75.0, 194: 150.0, 198: 60.0, 214: 90.0, 230: 120.0, 248: 60.0, 182: 135.0, 246: 60.0, 98: 60.0, 339: 150.0, 238: 150.0, 130: 120.0, 97: 150.0, 310: 90.0, 82: 120.0, 250: 60.0, 60: 75.0, 94: 150.0, 193: 150.0, 140: 150.0, 160: 75.0, 148: 60.0, 220: 105.0, 202: 60.0, 152: 60.0, 309: 90.0, 135: 135.0, 81: 120.0, 124: 105.0, 23: 105.0, 10: 75.0, 13: 75.0, 96: 150.0, 210: 90.0, 240: 150.0, 57: 75.0, 296: 60.0, 45: 150.0, 319: 105.0, 103: 60.0, 36: 135.0, 308: 90.0, 20: 90.0, 303: 75.0, 75: 105.0, 200: 60.0, 77: 120.0, 338: 150.0, 149: 60.0, 302: 75.0, 2: 60.0, 52: 60.0, 262: 90.0, 253: 75.0, 259: 90.0, 183: 135.0, 151: 60.0, 312: 90.0, 190: 150.0, 74:105.0, 243: 150.0, 87: 135.0, 239: 150.0, 143: 150.0, 286: 135.0, 266: 105.0, 136: 135.0, 166: 90.0, 83: 120.0, 155: 75.0, 279: 120.0, 126: 120.0, 195: 150.0, 265: 90.0, 318: 105.0, 104: 60.0, 153: 60.0, 282: 135.0, 226: 120.0, 25: 105.0, 196: 60.0, 64: 90.0, 15: 90.0, 297: 60.0, 109: 75.0, 26: 105.0, 76: 105.0, 43: 150.0, 280: 135.0, 3: 60.0, 49: 60.0, 333: 135.0, 30: 120.0, 121: 105.0, 115: 90.0, 320: 105.0, 216: 90.0, 264: 90.0, 209: 75.0, 1: 60.0, 313: 90.0, 22: 105.0, 317: 105.0, 7: 75.0, 141: 150.0, 86: 135.0, 241: 150.0, 215: 90.0, 68: 90.0, 50: 60.0, 156: 75.0, 252: 75.0, 254: 75.0, 276: 120.0, 178: 120.0, 281: 135.0, 237: 135.0, 71: 105.0, 129: 120.0, 144: 150.0, 335: 135.0, 133: 135.0, 203: 75.0, 255: 75.0, 72: 105.0, 235: 135.0, 37: 135.0}, 
'PEG-8000': {306: 6.0, 340: 6.0, 291: 5.0, 102: 2.0, 289: 5.0, 267: 5.0, 125:2.0, 11: 0.0, 146: 2.0, 229: 4.0, 165: 3.0, 263: 5.0, 287: 5.0, 159: 3.0, 95: 1.0, 67: 1.0, 4: 0.0, 247: 5.0, 65: 1.0, 85: 1.0, 222: 4.0, 211: 4.0, 330: 6.0, 292: 5.0, 91: 1.0, 6: 0.0, 217: 4.0, 169: 3.0, 331: 6.0, 90: 1.0, 117: 2.0, 106: 2.0, 256: 5.0, 138: 2.0, 107: 2.0, 174: 3.0, 132: 2.0, 18: 0.0, 315: 6.0, 92: 1.0, 80: 1.0, 127: 2.0, 123: 2.0, 251: 5.0, 294: 6.0, 236: 4.0, 131: 2.0, 322: 6.0, 197: 4.0, 111: 2.0, 154: 3.0, 189: 3.0, 122: 2.0, 120: 2.0, 328: 6.0, 208: 4.0, 301: 6.0, 73: 1.0, 59: 1.0, 12: 0.0, 273: 5.0, 27: 0.0, 332: 6.0, 342: 6.0, 89: 1.0, 29: 0.0, 58: 1.0, 212: 4.0, 93: 1.0, 150: 3.0, 105: 2.0, 112: 2.0, 162: 3.0, 327: 6.0, 305: 6.0, 283: 5.0, 179: 3.0, 119: 2.0, 14: 0.0, 245: 5.0, 191: 3.0, 261: 5.0, 51: 1.0, 9: 0.0, 242: 4.0, 16: 0.0, 188: 3.0, 0: 0.0, 249: 5.0, 187: 3.0, 62: 1.0, 171: 3.0, 278: 5.0, 234:4.0, 70: 1.0, 177: 3.0, 204: 4.0, 41: 0.0, 244: 4.0, 206: 4.0, 231: 4.0, 329: 6.0, 161: 3.0, 39: 0.0, 288: 5.0, 78: 1.0, 232: 4.0, 192: 3.0, 324: 6.0, 17: 0.0, 257: 5.0, 224: 4.0, 88: 1.0, 167: 3.0, 272: 5.0, 42: 0.0, 334: 6.0, 172: 3.0, 139: 2.0, 163: 3.0, 186: 3.0, 5: 0.0, 225: 4.0, 175: 3.0, 38: 0.0, 233: 4.0, 180: 3.0, 158: 3.0, 341: 6.0, 147: 3.0, 100:2.0, 34: 0.0, 110: 2.0, 218: 4.0, 321: 6.0, 19: 0.0, 213: 4.0, 44: 0.0, 314: 6.0, 207: 4.0, 185: 3.0, 108: 2.0, 299: 6.0, 79: 1.0, 325: 6.0, 201: 4.0, 8: 0.0, 285: 5.0, 99: 2.0, 300: 6.0, 293: 5.0, 275: 5.0, 28: 0.0, 31: 0.0, 55: 1.0, 32: 0.0, 219: 4.0, 48: 0.0, 284: 5.0, 227: 4.0, 33: 0.0, 35: 0.0, 260: 5.0, 63: 1.0, 157: 3.0, 128: 2.0, 46: 0.0, 66: 1.0, 274: 5.0, 173: 3.0, 326: 6.0, 336: 6.0, 277: 5.0, 269: 5.0, 168: 3.0, 47: 0.0, 113: 2.0, 268: 5.0, 40: 0.0, 21: 0.0, 101:2.0, 164: 3.0, 69: 1.0, 53: 1.0, 137: 2.0, 24: 0.0, 304: 6.0, 184: 3.0, 134: 2.0, 270: 5.0, 116: 2.0, 205: 4.0, 142: 2.0, 295: 6.0, 199: 4.0, 316: 6.0, 56: 1.0, 61: 1.0, 271: 5.0, 221: 4.0, 223: 4.0, 84: 1.0, 181: 3.0, 228: 4.0, 114: 2.0, 311: 6.0, 290: 5.0, 323: 6.0, 118: 2.0, 258: 5.0, 170: 3.0, 145: 2.0, 337: 6.0, 298: 6.0, 54: 1.0, 176: 3.0, 307: 6.0, 194: 3.0, 198: 4.0, 214: 4.0, 230: 4.0, 248: 5.0, 182: 3.0, 246: 5.0, 98: 2.0, 339: 6.0, 238: 4.0, 130: 2.0, 97: 1.0, 310: 6.0, 82: 1.0, 250: 5.0, 60: 1.0, 94: 1.0, 193: 3.0, 140: 2.0, 160: 3.0, 148: 3.0, 220: 4.0, 202: 4.0, 152: 3.0, 309: 6.0, 135: 2.0, 81: 1.0, 124: 2.0, 23: 0.0, 10: 0.0, 13: 0.0, 96: 1.0, 210: 4.0, 240: 4.0, 57: 1.0, 296: 6.0, 45: 0.0, 319: 6.0, 103: 2.0, 36: 0.0, 308: 6.0, 20: 0.0, 303: 6.0, 75: 1.0, 200: 4.0, 77: 1.0, 338: 6.0, 149: 3.0, 302: 6.0, 2: 0.0,52: 1.0, 262: 5.0, 253: 5.0, 259: 5.0, 183: 3.0, 151: 3.0, 312: 6.0, 190: 3.0, 74: 1.0, 243: 4.0, 87: 1.0, 239: 4.0, 143: 2.0, 286: 5.0, 266: 5.0, 136: 2.0, 166: 3.0, 83: 1.0, 155: 3.0, 279: 5.0, 126: 2.0, 195: 3.0, 265: 5.0, 318: 6.0, 104: 2.0, 153: 3.0, 282: 5.0, 226: 4.0, 25: 0.0, 196: 4.0, 64: 1.0, 15: 0.0, 297: 6.0, 109: 2.0, 26: 0.0, 76: 1.0, 43: 0.0,280: 5.0, 3: 0.0, 49: 1.0, 333: 6.0, 30: 0.0, 121: 2.0, 115: 2.0, 320: 6.0, 216: 4.0, 264: 5.0, 209: 4.0, 1: 0.0, 313: 6.0, 22: 0.0, 317: 6.0, 7: 0.0, 141: 2.0, 86: 1.0, 241: 4.0, 215: 4.0, 68: 1.0, 50: 1.0, 156: 3.0, 252: 5.0, 254: 5.0, 276: 5.0, 178: 3.0, 281: 5.0, 237: 4.0, 71: 1.0, 129: 2.0, 144: 2.0, 335: 6.0, 133: 2.0, 203: 4.0, 255: 5.0, 72: 1.0, 235: 4.0, 37: 0.0}
}

################################################################################

# Total number of samples (max. 343 combinations)
nsamples = len(Mg_final_conc)**3 + 1

def run(protocol):
    
    ## Load instrument, modules and labware ##

    #--------------#--------------#--------------#
    # 2mLEppendorf #   384-well   #    Trash     #
    #  tubes, 4C   #   plate      #              #
    #--------------#--------------#--------------#
    #              #   P20 tips   #  P300 tips   #
    #              #              #              #
    #------------- #------------- #------------- #
    # PCR strips,  # 15mL falcon  #              #
    # 4C           # rack         #              #
    #------------- #------------- #------------- #
    #              #              #              #
    #              #              #              #
    #------------- #------------- #------------- #


    # Pipettes and tips
    tips20 = protocol.load_labware('opentrons_96_tiprack_20ul', 8)
    tips300 = protocol.load_labware('opentrons_96_tiprack_300ul', 9)
    p20 = protocol.load_instrument('p20_single_gen2', mount='left', tip_racks=[tips20])
    p300 = protocol.load_instrument('p300_single', mount='right', tip_racks=[tips300])

    # 384-well plate
    plate = protocol.load_labware('corning_384_wellplate_112ul_flat', 11)
    
    # Tube rack
    rack = protocol.load_labware ('opentrons_15_tuberack_falcon_15ml_conical', 5)

    # Temperature modules
    temp_module_pcrtubes = protocol.load_module('temperature module gen2', 10)
    pcrtubes_cool = temp_module_pcrtubes.load_labware('opentrons_96_aluminumblock_generic_pcr_strip_200ul')
    #temp_module_pcrtubes.set_temperature(4)

    temp_module_eppendorftubes = protocol.load_module('temperature module gen2', 4)
    eppendorftubes_cool = temp_module_eppendorftubes.load_labware('opentrons_24_aluminumblock_nest_2ml_snapcap')
    #temp_module_eppendorftubes.set_temperature(4)  
    
    ## Define start reagents

    # In Eppendorf module
    # A1. DNA: 200 muL
    # A2. Buffer: 1.5 mL
    # A3. Lysate: 2 mL
    # A4. MilliQ: 2 mL
    # B1. Mg-glutamate: 100 muL 1M
    # B2. K-glutamate: 300 muL 2M
    # B3. PEG-8000: 350 muL 40%
    DNA = eppendorftubes_cool.wells_by_name()["A1"]
    BufferW = eppendorftubes_cool.wells_by_name()["A2"]
    Lysate = eppendorftubes_cool.wells_by_name()["A3"]
    MQ = eppendorftubes_cool.wells_by_name()["A4"]
    Mg_glut = eppendorftubes_cool.wells_by_name()["B1"]
    K_glut = eppendorftubes_cool.wells_by_name()["B2"]
    PEG8000 = eppendorftubes_cool.wells_by_name()["B3"]

    # In rack
    MM = rack.wells_by_name()["A1"]
    
    # Tip tracker
    p20_st = 1
    p300_st = 1
    p20.starting_tip = tips20.wells()[p20_st]
    p300.starting_tip = tips300.wells()[p300_st]

    def find_index(lst,item):
        if item in lst:
            return lst.index(item)
        else:
            return None   

    def sorted_factors_to_lst(factors,reagent):
        """Extract factor values from pandas dataframe.
        Input is a string with name of reagent and outputs a sorted list"""
        lst = factors[reagent].tolist()
        lst.sort()
        return lst

    def pipette_viscious(mode):
        """Decrease flow rate for pipettes suitable for vicous liquids."""
        if mode == 0:     # OFF
                p20.flow_rate.aspirate = 7.56
                p20.flow_rate.dispense = 7.56
                p300.flow_rate.aspirate = 92.86
                p300.flow_rate.dispense = 92.86
        if mode == 1:     # ON
                p20.flow_rate.aspirate = 2
                p20.flow_rate.dispense = 2
                p300.flow_rate.aspirate = 10
                p300.flow_rate.dispense = 10

    def transfer_small_vol_to_well(well_start, well_stop, reagent,p20_st):
        """Transfer 0.5 uL of reagent to a range of destination wells in the well plate."""
        p20.pick_up_tip(tips20.wells()[p20_st])
        total_vol = ((well_stop - well_start) * 0.5) + 1
        if total_vol >= 38:
            i = 0
            while i < well_stop:
                if i+38 < well_stop:
                    p20.aspirate(location=reagent.bottom(1))
                    for well_no in range(i, i+38):
                        p20.dispense(0.5, plate.wells()[well_no].bottom(0.1))
                else:
                    p20.blow_out(reagent)
                    p20.aspirate((well_stop-i) * 0.5, reagent.bottom(1))
                    for well_no in range(i, well_stop):
                        p20.dispense(0.5, plate.wells()[well_no].bottom(0.1))
                i+=38
        else:
            p20.aspirate(total_vol, reagent.bottom(1))
            for well_no in range(well_start, well_stop):
                p20.dispense(0.5, plate.wells()[well_no].bottom(0.1))
        p20.drop_tip()
    
    def transfer_combinations_of_small_vol_to_well(well_no_lst, reagent, vol, p20_st):
        """Transfer a small volume down to 0.5 uL of reagent to a list of destination 
        wells in the well plate."""
        p20.pick_up_tip(tips20.wells()[p20_st])
        i = 0
        if vol == 0.5:
            dispenses_pr_fill = 38
        elif vol == 0.75:
            dispenses_pr_fill = 24
        elif vol == 1.5:
            dispenses_pr_fill = 12
        while i < len(well_no_lst):
            if i+dispenses_pr_fill < len(well_no_lst):
                p20.aspirate(location=reagent.bottom(1))
                for well_no in well_no_lst[i:i+dispenses_pr_fill]:
                    p20.dispense(vol, plate.wells()[well_no].bottom(0.1))
                p20.blow_out(reagent)
            else:
                p20.aspirate((len(well_no_lst)-i) * vol, reagent.bottom(1))
                for well_no in well_no_lst[i:len(well_no_lst)]:
                    p20.dispense(vol, plate.wells()[well_no].bottom(0.1))
            i+=dispenses_pr_fill
        p20.drop_tip()
    
    def make_single_dilution(vol,reagent_stock,row,p20_st):
        """Dilute the stock concentration to the reference concentration if not part of the serial dilutions."""
        p20.pick_up_tip(tips20.wells()[p20_st])
        p20.transfer(vol, reagent_stock, pcrtubes_cool.wells()[row], touch_tip=True, new_tip="never")
        p20.drop_tip()
        p20.pick_up_tip(tips20.wells()[p20_st+1])
        p20.transfer(10-vol, MQ, pcrtubes_cool.wells()[row], touch_tip=True, mix_after=(5,5), new_tip="never")
        p20.drop_tip()

    def load_control(factors,p20_st):
        """Load the internal control (without DNA) to the well plate with 3 mM Mg-glutamate, 
        60 mM K-glutamate, and 2% PEG-8000."""

        # No DNA
        p20.pick_up_tip(tips20.wells()[0])
        p20.aspirate(1,MQ)
        p20.dispense(0.5, plate.wells()[nsamples])
        p20.drop_tip()

        # Add reference factors
        Mg_final_conc = sorted_factors_to_lst(factors,'Mg-glutamate')
        K_final_conc = sorted_factors_to_lst(factors,'K-glutamate')
        P_final_conc = sorted_factors_to_lst(factors,'PEG-8000')
        if find_index(Mg_final_conc,3) is not None:
            dil_well = "A{}".format(find_index(Mg_final_conc,3)+2)
        else:
            # Make dilution and add to well
            dil_well = "A1"
            make_single_dilution(0.6,Mg_glut,0,p20_st)
            p20_st += 2
        p20.pick_up_tip(tips20.wells()[p20_st])
        p20.transfer(0.5, pcrtubes_cool.wells_by_name()[dil_well], plate.wells()[nsamples], touch_tip=True, new_tip="never")
        p20.drop_tip()
        p20_st += 1
        if find_index(K_final_conc,60) is not None:
            dil_well = "B{}".format(find_index(K_final_conc,60)+2)
        else:
            # Make dilution and add to well
            dil_well = "B1"
            make_single_dilution(4,K_glut,1,p20_st)
            p20_st += 2
        p20.pick_up_tip(tips20.wells()[p20_st])
        p20.transfer(0.75, pcrtubes_cool.wells_by_name()[dil_well], plate.wells()[nsamples], touch_tip=True, new_tip="never")
        p20.drop_tip()
        p20_st += 1
        if find_index(P_final_conc,2) is not None:
            dil_well = "C{}".format(find_index(P_final_conc,2)+2)
        else:
            # Make dilution and add to well
            dil_well = "C1"
            make_single_dilution(3.3,PEG8000,2,p20_st)
            p20_st += 2
        p20.pick_up_tip(tips20.wells()[p20_st])
        p20.transfer(1.5, pcrtubes_cool.wells_by_name()[dil_well], plate.wells()[nsamples], touch_tip=True, new_tip="never")
        p20.drop_tip()
        p20_st += 1

        return p20_st
        
    def calc_volume(reagent, final_conc_lst, stock_conc, final_vol, dil_factor):
        """
        Calculate volumes of reagent stock/dilution to get final concentration.
        Takes in a list of final concentrations, final volume, name of reagent and dilution factor
        and outputs two lists with volumes of stock/dilution and MilliQ.
        """
        reagent_vol_lst = []
        mq_vol_lst = []
        for i in range(len(final_conc_lst)):
            vol = ((final_conc_lst[i]*dil_factor)*final_vol)/stock_conc
            if vol > final_vol:
                raise ValueError("Error: Stock volume exceeds 30 muL. Change {} stock concentration.".format(reagent))
            elif vol < 0.5 and vol != 0:
                raise ValueError("Error: Stock volume lower than minimum required volume 0.5 muL. Change {} stock concentration.".format(reagent))
            else:
                if final_vol == ceil(vol):
                    reagent_vol_lst.append(ceil(vol))
                    mq_vol_lst.append(0)
                else:
                    if final_vol-vol < 0.5:
                        raise ValueError("Error: MilliQ volume lower than minimum required volume 0.5 muL. Change {} stock concentration.".format(reagent))
                    else:
                        reagent_vol_lst.append(vol)
                        mq_vol_lst.append(final_vol-vol)
        return reagent_vol_lst, mq_vol_lst
    
    def add_MQ(MQ_vol_lst,row):
        """Adds MilliQ to serial dilution, designed to reuse tips to save plastic."""
        if any(vol > 20 for vol in MQ_vol_lst):
            for i in range(len(MQ_vol_lst)):
                if MQ_vol_lst[i] == 0:
                    pass
                elif MQ_vol_lst[i] <= 20:
                    p20.pick_up_tip(tips20.wells()[0])
                    p20.transfer(MQ_vol_lst[i], MQ, row[i+1], new_tip="never")
                    p20.return_tip()
                else:
                    p300.pick_up_tip(tips300.wells()[0])
                    p300.transfer(MQ_vol_lst[i], MQ, row[i+1], new_tip="never")
                    p300.return_tip()
        else:
            p20.pick_up_tip(tips20.wells()[0])
            p20.transfer(MQ_vol_lst, MQ, row[1:len(Mg_final_conc)+1], new_tip="never")
            p20.return_tip()
    
    def add_reagent(reagent_vol_lst,reagent_stock,row,p20_st,p300_st):
        """Adds and mixes reagent to serial dilution, designed to reuse tips to save plastic."""
        if any(vol > 20 for vol in reagent_vol_lst):
            for i in range(len(reagent_vol_lst)):
                if reagent_vol_lst[i] == 0:
                    pass
                elif reagent_vol_lst[i] <= 20:
                    p20.pick_up_tip(tips20.wells()[p20_st])
                    p20.transfer(reagent_vol_lst[i], reagent_stock, row[i+1], mix_after=(5,15), new_tip="never")
                    if i != len(reagent_vol_lst)-1:
                        if reagent_vol_lst[i+1] <= 20:
                            p20.return_tip()
                        else:
                            p20.drop_tip()
                    else:
                        p20.drop_tip()
                else:
                    p300.pick_up_tip(tips300.wells()[p300_st])
                    p300.transfer(reagent_vol_lst[i], reagent_stock, row[i+1], mix_after=(5,15), new_tip="never")
                    if i != len(reagent_vol_lst)-1:
                        if reagent_vol_lst[i+1] > 20:
                            p300.return_tip()
                        else:
                            p300.drop_tip()
                    else:
                        p300.drop_tip()
            p20_st += 1
            p300_st += 1
        else:
            p20.pick_up_tip(tips20.wells()[p20_st])
            p20.transfer(reagent_vol_lst, reagent_stock, row[1:len(Mg_final_conc)+1], mix_after=(5,15), new_tip="never")
            p20.drop_tip()
            p20_st += 1
        return p20_st, p300_st    

    def factors_dilution(factors,Mg_stock_conc,K_stock_conc,P_stock_conc,p20_st,p300_st):
        """Make dilutions of Mg-glut, Mg-glut and PEG-8000
        based on csv file input."""
        
        # Load reagent's final concentration
        Mg_final_conc = sorted_factors_to_lst(factors,'Mg-glutamate')
        K_final_conc = sorted_factors_to_lst(factors,'K-glutamate')
        P_final_conc = sorted_factors_to_lst(factors,'PEG-8000')

        # Prepare dilutions
        for i in range(3):
            row = pcrtubes_cool.rows()[i]
            if i == 0:    # Mg-glutamate
                (Mg_glut_vol_lst, MQ_vol_lst) = calc_volume("Mg-glutamate",Mg_final_conc,Mg_stock_conc,30,20) # final volume is 30 muL
                add_MQ(MQ_vol_lst,row)
                (p20_st,p300_st) = add_reagent(Mg_glut_vol_lst,Mg_glut,row,p20_st,p300_st)
            elif i == 1:  # K-glutamate
                (K_glut_vol_lst, MQ_vol_lst) = calc_volume("K-glutamate",K_final_conc,K_stock_conc,50,13) # final volume is 50 muL
                add_MQ(MQ_vol_lst,row)
                (p20_st,p300_st) = add_reagent(K_glut_vol_lst,K_glut,row,p20_st,p300_st)
            elif i == 2:  # PEG-8000
                (PEG8000_vol_lst, MQ_vol_lst) = calc_volume("PEG-8000",P_final_conc,P_stock_conc,80,6.66) # final volume is 80 muL
                add_MQ(MQ_vol_lst,row)
                pipette_viscious(1)  # ON
                (p20_st,p300_st) = add_reagent(PEG8000_vol_lst,PEG8000,row,p20_st,p300_st)
                pipette_viscious(0)  # OFF
        
        # Trash MQ 300 uL pipette tip
        p300.pick_up_tip(tips300.wells()[0])
        p300.drop_tip()
        return p20_st,p300_st

    def MM_vol(nsamples):
        """Adjust z-axis for mixing mastermix dependent on the number of samples"""
        return 0.1*(nsamples)

    def cfe_mastermix(p300_st):
        """Prepare mastermix excl. factors to optimize and loads to well plate.
        Mastermix consits of BufferW and lysate"""
         
        lysate_vol = 4 * nsamples * 1.3 #uL
        bufferW_vol = 3 * nsamples * 1.3  #uL
        p300.pick_up_tip(tips300.wells()[p300_st])
        p300.transfer(lysate_vol, Lysate, MM,  touch_tip=True, blow_out=True, blowout_location='source well', new_tip="never")
        pipette_viscious(1)  # ON
        p300.transfer(bufferW_vol, BufferW, MM, blow_out=True, blowout_location='source well', new_tip="never")
        pipette_viscious(0)  # OFF
        pos = MM_vol(nsamples)
        for i in range(20):
            p300.aspirate(300, MM.bottom(1))
            p300.dispense(300, MM.bottom(pos))
        p300.distribute(7, MM, plate.wells()[:nsamples+1], blow_out=True, blowout_location='source well', new_tip="never")
        p300.drop_tip()
        p300_st += 1 
        return p300_st 
    
    def load_combinations(factors, p20_st):
        """Makes a full factorial experimental design for the 3 factors
        Mg-glutamate, K-glutamate and PEG-8000. This is used to load
        all possible combinations. All wells with the same condition 
        for a factor is loaded simultanously to the 384-well plate. 
        Input is the csv file with factors."""

        ff = pd.DataFrame.from_dict(ff_dict)
        Mg_final_conc = sorted_factors_to_lst(factors,'Mg-glutamate')
        K_final_conc = sorted_factors_to_lst(factors,'K-glutamate')
        P_final_conc = sorted_factors_to_lst(factors,'PEG-8000')

        # Add Mg-glutamate combinations
        for i in range(len(Mg_final_conc)):
            conc_i = ff["Mg-glutamate"]==Mg_final_conc[i]
            conc_i_wells = []
            [conc_i_wells.append(j) for j in range(len(conc_i)) if conc_i.tolist()[j] ]
            dil_well = "A{}".format(i+2)
            transfer_combinations_of_small_vol_to_well(conc_i_wells, pcrtubes_cool.wells_by_name()[dil_well], 0.5, p20_st)
            p20_st += 1

        # Add K-glutamate combinations
        for i in range(len(K_final_conc)):
            conc_i = ff["K-glutamate"]==K_final_conc[i]
            conc_i_wells = []
            [conc_i_wells.append(j) for j in range(len(conc_i)) if conc_i.tolist()[j] ]
            dil_well = "B{}".format(i+2)
            transfer_combinations_of_small_vol_to_well(conc_i_wells, pcrtubes_cool.wells_by_name()[dil_well], 0.75, p20_st)
            p20_st += 1

        # Add PEG-8000 combinations
        pipette_viscious(1)  # ON
        for i in range(len(P_final_conc)):
            conc_i = ff["PEG-8000"]==P_final_conc[i]
            conc_i_wells = []
            [conc_i_wells.append(j) for j in range(len(conc_i)) if conc_i.tolist()[j] ]
            dil_well = "C{}".format(i+2)
            transfer_combinations_of_small_vol_to_well(conc_i_wells, pcrtubes_cool.wells_by_name()[dil_well], 1.5, p20_st)
            p20_st += 1
        pipette_viscious(0)  # OFF
        return p20_st


    ## Protocol workflow
    
    # Dilute factors
    factor_dict = {"Mg-glutamate": Mg_final_conc, "K-glutamate": K_final_conc, "PEG-8000":P_final_conc}
    factors = pd.DataFrame (factor_dict)
    (p20_st,p300_st) = factors_dilution(factors,Mg_stock_conc,K_stock_conc,P_stock_conc,p20_st,p300_st)

    # Prepare and load buffer mix excl. factors for optimization
    p300_st = cfe_mastermix(p300_st)

    # Load control wo/ DNA and reference concentration for all factors
    p20_st = load_control(factors,p20_st)

    # Load combinations of factors
    p20_st = load_combinations(factors, p20_st)
    
    # Add DNA to initiate cell-free expression
    transfer_small_vol_to_well(0, nsamples, DNA, p20_st)

    #temp_module_pcrtubes.deactivate()
    #temp_module_eppendorftubes.deactivate()
