#!/usr/bin/awk
BEGIN {
    FS = ":"
}
{
    # A == after context
    # B == before context
    hitln = $2
    startln = hitln - B > 0 ? hitln - B : 0
    endln = hitln + A
    print "-r " startln ":" endln " -H " hitln " " $1
}
