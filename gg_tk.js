var QL = function(a) {
    return function() {
        return a
    }
}
SL = null;
mf = "=";
k = "";
cb = "&";

var d = QL(String.fromCharCode(116)),c = QL(String.fromCharCode(107)),d = [d(), d()];
c = "&" + d.join("") + "=";

RL = function(a, b) {
    for (var c = 0; c < b.length - 2; c += 3) {
        var d = b.charAt(c + 2);
        d = "a" <= d ? d.charCodeAt(0) - 87 : Number(d);
        d = "+" == b.charAt(c + 1) ? a >>> d : a << d;
        a = "+" == b.charAt(c) ? a + d & 4294967295 : a ^ d
    }
    return a
}
Vb = "+-a^+6"
Ub = "+-3^+b+-f"
dd = "."
tkk = [406398, 561666268 + 1526272306]



md5 = function(a) {
    var b;
    if (null === SL) {
        var c = QL(String.fromCharCode(84));//T
        b = QL(String.fromCharCode(75));//K
        c = [c(), c()];

        c[1] = b();
        SL = Number(window[c.join(b())]) || 0;
    }
    b = tkk[0];

    var d = QL(String.fromCharCode(116))
        , c = QL(String.fromCharCode(107))
        , d = [d(), d()];
    d[1] = c();
    for (var c = cb + d.join(k) +
        mf, d = [], e = 0, f = 0; f < a.length; f++) {
        var g = a.charCodeAt(f);
        128 > g ? d[e++] = g : (2048 > g ? d[e++] = g >> 6 | 192 : (55296 == (g & 64512) && f + 1 < a.length && 56320 == (a.charCodeAt(f + 1) & 64512) ? (g = 65536 + ((g & 1023) << 10) + (a.charCodeAt(++f) & 1023),
                        d[e++] = g >> 18 | 240,
                        d[e++] = g >> 12 & 63 | 128) : d[e++] = g >> 12 | 224,
                    d[e++] = g >> 6 & 63 | 128),
                d[e++] = g & 63 | 128)
    }
    a = b || 0;

    for (e = 0; e < d.length; e++)
        a += d[e],
            a = RL(a, Vb);
    a = RL(a, Ub);
    a ^=tkk[1];
    0 > a && (a = (a & 2147483647) + 2147483648);
    a %= 1E6;
    return c + (a.toString() + dd + (a ^ b))
}
