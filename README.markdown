PyJDPA
======

PyJDPA is a snippets used to parse [JDPA Sentiment
Corpus](https://verbs.colorado.edu/jdpacorpus/) to TSV format. The snippet is
written in Python.

    Usage: pyjdpa.py [options] doc_id rel_type. E.g: pyjdpa.py camera-002-002 target

    Options:
      -h, --help            show this help message and exit
      -d PATH, --data-path=PATH
                            Path to JDPA data dir. Default is ../data
      -H, --no-header       Don't display header line
      -s SLOT_MENTION, --slot-mention=SLOT_MENTION
                            Slot mention type: 'string' (stringSlotMention)
                            or'complex' (complexSlotMention). Default is
                            'complex'.


Explanation:
  - doc_id: is the prefix of a doc file name (e.g. doc_id of 
    "camera-002-002.txt" is "camera-002-002").
  - rel_type: is the type of stringSlotMention->mentionSlot or 
    complexSlotMention->mentionSlot that you want to extract.
  - --data-path: is the path to the fold which contains JDPA data. This folder
    should contain sub-folders [camera], [car], [doc].
  
Example:

The command `$ python pyjdpa.py camera-002-002 target` should print:

    arg0    rel arg1    arg0_start  arg0_end    arg1_start  arg1_end
    answered    target  quick start guide   1308    1316    1325    1342
    pretty  target  pictures    2404    2410    2411    2419
    wedded  target  brand   454 460 477 482
    many    target  bells/whistles  705 709 710 724
    many    target  bells/whistles  705 709 710 724
    respected   target  electronics brand   645 654 655 672
    cheap   target  they    255 260 243 247
    little  target  Sony    1733    1739    1740    1744
    heavy   target  it  2630    2635    2614    2616
    new target  they    817 820 808 812
    20% off target  camera bag  3417    3424    3405    3415
    pretty  target  pictures    2375    2381    2382    2390
    pleased target  taking pictures 1162    1169    1217    1232
    pleased target  charge  1162    1169    1188    1194
    heavy   target  they    1832    1837    1823    1827
    hassle  target  it  3709    3715    3007    3009
    friendly    target  sales person    2239    2247    2248    2260
    competitive target  Sony    837 848 822 826
    Happy   target  Mother's Day    1029    1034    1035    1047
    free    target  value   3110    3114    3093    3098
    nicely  target  shutters    2960    2966    2951    2959
    expensive   target  Canons  746 755 756 762
    expensive   target  Nikons  746 755 766 772
    happy   target  photos  1708    1713    1718    1724
    fine    target  3 frame per second  2977    2981    2912    2930
    steep   target  price   789 794 795 800
    competitive target  prices  2033    2044    2004    2010
    respected   target  store   1920    1929    1937    1942
    comment target  photos  1433    1440    1465    1471
    better  target  price   429 435 413 418
    huge    target  camera sale 1881    1885    1903    1914
    best    target  plus lens   2995    2999    3042    3051
    best    target  zoom lens   2995    2999    3069    3078


