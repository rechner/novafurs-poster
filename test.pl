
# *emphasized (italic) →   s/\*([^*]+?)\*/[i]$1[\/i]/a
#                          s/[^\\]?\*([^*]+?)\*/\[i\]$1\[\/i\]/
# **bold text** →          s/\*\*([^*]+?)\*\*/[b]$1[\/b]/
# > quoted text →          s/^\s+?>

# <p style="color:#ff00ff">coloured text</p>
#       s/<p\ style="color:\#(.*)">(.*)+?<\/p>/[color=$1]$2[/color]/

$st = '*this* is a **test** of the \*test\*';

# Escapes
$st =~ s/\\\*/%%STRASTRISK%%/g;

# Strong must go first
$st =~ s/(\*\*|__)(?=\S)(.+?[*_]*)(?<=\S)\1/\[b\]$2\[\/b\]/g;
$st =~ s/(\*|_)(?=\S)(.+?)(?<=\S)\1/\[i\]$2\[\/i\]/g;

# Unescape
$st =~ s/\%\%STRASTRISK\%\%/\*/g;

print "\n" . $st . "\n\n";
