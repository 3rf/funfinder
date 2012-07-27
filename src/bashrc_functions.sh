
# 'goto' wrapper for funfinder allows you to quickly jump to a searched dir
function goto
{
    pushd `funfind --goto $1`
}
#alias funfinder to fun...what...DO YOU HATE FUN!?
alias fun='funfind'
