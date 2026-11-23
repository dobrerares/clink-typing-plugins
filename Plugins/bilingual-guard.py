# ---
# name: Bilingual Guard
# icon: text.badge.checkmark
# summary: Touch-aware Romanian + English autocorrect, diacritics, completions and next words
# version: 1.2
# author: Rares
# enabled: false
# ---

# Taps are scored against nearby keys (2D Gaussian, learned offsets); a beam search allows
# slips plus one missed/extra/swapped letter; word pairs and the recent language weigh it;
# a word is replaced only when the best reading beats it by a margin (large for real words).
# Clink's fix decides words this list lacks; learned letter rules add Romanian diacritics to
# them. Design adapted from Hex's TypingDecoder (github.com/anomalyco/hex, MIT,
# (c) 2026 Christopher Langton). DATA_*/PAIRS/ENDS/RULES adapt
# FrequencyWords (OpenSubtitles 2018, Hermit Dave, CC BY-SA 4.0) and Tatoeba (CC BY 2.0
# FR) counts; shared under CC BY-SA 4.0. No Google/Gboard data. Internally A=ă Q=â I=î S=ș T=ț.

import math
import re

DATA_RO = """@AACStia!ia1MlaOea1Lsta0LISi1JTi1Ji1Jl[mbolnAvit^rATiSat&cat}A_ac6Ti^unAtATi2Ii]pArTim=t`at|ul3TiedicA}a?t_nge;s^lini^otrivA8Na3LreunA|a_umuTi)t>a?t}e^uSc{aWt1En]AlTime>aEuntru]Sel&at;i^iSi_ne4TvA.TeleagA|ptA6Mg7Ne>Ti>m*re?ea7Ni<pciune=t6Ms2Kainte)a^lTiRt;A3Lpoi2JcA_lcat4TpATQnatA_rcatPQntat>A4Nt/a$eapA5NrcAFp`Qnd5Me{TiHm&i5LutWul4NrcVAm(QndHa=Ti=m)re~a7Mt<eHi4Nt`a{Ti(tUeazA{zi/heiat{e_iSi;d{AHe|Ti;riatGs(A<eHoare~ea;zi$oace:lo_tro3Mredere+a^uiat|A#datA/eajuns:pArtat}eazA`lini~tPoialA`eli(sc^rAgostesc+it~itA;zneSti:eaptA`ptat.ecat2Tflorit/ricoSAtor.ger`ul^heTat*A}a`aTA_iTit/rijora~TiYt?tA}eazA_opat`zitoare?r.mormQntare.nebunit.oTi^atA;ePt_Am:a]registrAri~are~area?atDsA_Si%rcinatA/cris3LeamnA:mna|t{e3ToTi{t^pre$uSi%Ti:mi_rat2NtQi_lneSte?i|ascAWscViWmJre+a>i~le7Nt4MmplA7Na>re8LtWe:rziaKt|e>re=i/eleg|i<s/inde;s$oarcA7Me}TiXm}re4NrcVi5Ns4Ltdeauna3Lr4Me&abA<gAJa5Nb{AmJri?le(a|Ti)m7NreYa7NtVi&g(i7Ti=me(ul`rup}t_u^unecat?AVricDvAT;AmUa<Ti{rea6NtPaTA$eTeUi^iat_nge`s[s]iNtiZSah.mpanie2NnsA%a:e;leDpte.rpe2Nse1McoalAGa^li;i5Tle1Tederea/inTA{a#f$uFl;e`ui]rif`ul^pi1Ei.r[o]arece{i]c^at#fer;ul]setele-terge:sDi3NTiEa:TiFi4Nm:u3Ke3Ji%nTA<a{ifice`d3Nm^re%i`le3Iu4NtMTAri:i_le1NarAEa1KiDe]gAri/arADiDn$A3Le:Ti_a:m^tA:aEut.pA^a_t/i0Ea1JS2Ha$dar#ezat2MteaptARpTi5NtHAmHaWTi|iWm=reJt(e1KTi1Tah-bTine.andonat]by2Nia^litATile{atea]ordare]senTa`tEolut`vire=t^urd{A]undente[cTioneazA%une|a{i=le2KasA]cent{ul:pTi;t<A(a|TiWt{e%sEident}e*ul~luiDeSti(a3Ma4JstA6La3Mea5NSiPi:a;Si3Ml4Na5NSiFe;a(Si`i:ui3Jst`A5La5Le6NaHi&or|aGui2Jolo^perA{i)S}ul7TTi=re)t}A3Mrd;at.t^e:le^iv`itATi~ile|ate^or^riTA/ualA2Ium_a^zaTii&t-dApost/ugatOQnc`A#amPptareaOeseaPvAr6LatXA>a>e>ul6Mul2MicA$o]mir]n]optat$r_A%mit.resAUa#u3Nc%AFe;Ti;mRi^lTi:t^nA:at3NsCer$oport}ul$ulNfacere)aHi=le3LrA%a]ectat;eazA2NlA%m$a_TiFt$e$iPu#rica[gATat]enTi{a{e{iRt&ul]itat]lomeratCh]a1Gi2La2NbA2Hci.ureaCjuTiEngUA5MeVmUi4Ms3NtFA&m4Ma;TiGt4Ne4Mor6Nul1JlDAturi#TiFi.an/rmADbPA^aStri%strAWu/e_rt/i_nele.cool2Me/a:rgA^e/gRe&re=a{i=le:i/rg;a<t5Te`i{c3Ns$x#geria]i^bi/ce^menteDo2Nt3MAPa3Nceva4Nineva_uiva3Ne%le:rnativAEfel/or;a/uiaFl_ndeva1Fm2NQndoi(uA.abil/ndaObele^iTios_i^ulanTA.eTit^ndA:inTare>tPricaWn>A>i~i<ii/stec#iazA;aEce^nFte(SteKi6Nsc&i<Ti{m{re=i}le<t]prentA|e}leDuzant|A.y1Nn]a^lizA.chetA.d^rew/y]gajaTi8TiVt`eazA^ela`es$lia2Ji$i^lorPmalVe)le8Tor^versarea]n/a^e/ie]terioare|r^ic^renament{or>ul2Nul:at%uiPme:it{A(e$nT`a{t1MpA^rArii_a;re|a`t:eaFut^saTi2Na$r:A_TinWe_at<ul%e;nt_i`TiaRtamentYtul^sA.ei$l:e_ul^re]licA`aTie2Loi.recia(ez$ilie_nde;s3Loape_bat:pia=Ti)t}AVe=re~a{i&oRximativ]ucA:at1HrDATiEt_AmFa;TiUt2Tanja<t3MtA%e#de2IePstat.gint^umentul]ipi2NmA$aRtA;a`eiPe%le]ogant#s#tA/a/hur/icol|e=ul:ficialA~le:st.uncUA{m`a<TiVt`e`i[scuTitRlTi&t6NA|mVa)Ti)t{e:nd<AVeUs{A{e&ziDearA^mAnAtoare4Menea]ia$gur<A|m<a=re|t^stent>A}a2LtAzi3Ga3Lea`ptA3Nfel]um3Npra-tQTia3JtFaReaOac:A%at_ul.enTi(aHeFt;A^rizat.ingUe;iRs^tudine~a2TmosferA>a]rage:s2Kunci1Hu2Nd$A/e.gustDr/ulDstralia.toRbuzJul_mat_r5Titatea;ul_stradA2Nzi:Ti:m4Lt!vQnd]ans`at_taj2MeTi3Ka%i4NmRu3Km/nturA
/re_tisment<zat=ez]ioaneRnUul]ocaTiUt(ul2Kut1Lzi^lBbA.T.ga%t]iEatGul^eTel5NiViRte`i2Tnci$uiescOrbaTiWi5NtHul]tAlia{e$aiePrQn{A{e{i(ulPutDut%urA{a<i!a.Ti]by]ftA.g^A^aje<le`ul/i.iaEe]l^con$tA.nPcA:a^dA:a3Li4Mi_lor#r/A^ba$cA:a^ry^ul.schet/eball.tAPe_m_ria.zAEa^eazA-eTi2Na$tEu.beluS=ulOi#m#n^zi;nAOre_a/lin]th^ty[iblia`e&otecA~a#cicletAXa]etul]g]juterii9Tle#let;e<le;ul$l%y2HneFInTeles_cuvQnteze%le_venitDrouGl{ui]scuiTiPericA|a|ii[lestemat#ocat{A3TndA!oalA:aOb$by.gaTiRt&A]li_iEnav(A{i#mbA_oane.rd2Mston{ul!rQnzA;a]aT:e;le:ul^d3TndonPvoPzilia}n.ian]oasca^oklyn^wn]ucePsc1TuStean.cATi:tAriaXe;ar$atA3Nur&A{m`at`eSti`i{a(e&os2Kn3JA3Me3NiRca;ii5ToUul|e|ui^ul_ri]rsA.ton`ul]ze:le/unar|ul[y0EcA]Tea]cat$i.dea_rea.i]lAtoreSti}ascA>sc=i*aXe}i>t^cat^durA<a.maSA;a3Tin]pSuni$itanWeWul~ui2NrTi`iGle/ei`a$or`a$ui;a]sAtoreSte?ti>ascA*sc)i>Ti>a*e}mKt2Ntre#utAm_Qnd%a&Ti;m`re)aUtDzut!Ind]t-QStig(A|mHaJt(e<iDTiFvaDine5Nle:i&i.mp_ul.nTi3Hd:vaPtRA`m;reT_QndRa`t%eUc{e(ul2Jt^A3MeRodatA4Lva1Ha]binA^lul`rile]d/A^a_vre<u)l/eEou`l;ri/rul2NfeaUua_nea.iiOl^ci_ulatoare~arele?r+rulEd:A3NeFa/ifornia%tate}aPm_a_i/ul2Mm3NerA5Ma&e{i<le/ion<ul^panie_ionatul]nada`ian_l`ul:pea|ua$cer2NpPAt`ulPabil|A_citatea^canA<a^ete/italA)a3Nul`ui]r3Tacterul/dul3Ge/ierA<a/l_osPne&a^ol^rie3Mte5Ma;r%ier|ul:ofi|i2LsA3La$eRi:le_tA_y/tel<ul]tegoric^herineOuTi^ciucEtFA%e$zA4Ma`t{e2Nz3Ti3Nul:ri1Fe2La/ScAEi%ulElaltA/rA%tAPsFul]cul2Kea2LiElalTi2JlPAlalt3Le:bru_i%lalteEor`lalTi$ui_lA`a`e2TnTi^tral|A&uVl^uSa2Nr^c_ei`tAri{areEe_Ti_ale:m`onia:re<aPi^t_Am%atPul4Nt2Iva.zar!harlesUie`otteDeamA$fPia:eRle/ltuit/m:a`TiUt_iEstia(e(i=le<une2Jiar/cago$na_ezA{esc3Tp:eS_ul/ria/tarA]loe#ris`tine.uck1Ni]a]mitirDnAPa3Mci`sprezece;zeci3Je:ma4Kva/ste&it]oc%olatA>a]rcumstanTeOteSteViRascAFscPi:Ti_nd4Nt;ul/yOuda5Nt(A<e]vil!lAdire)a{i=i|le.aireEr:A_e:kEsA%a_ei:icA.ienTi=i;t<ul^nicAEpA#ub:ul{ui[oS/mar^ul.adA_a3TstA`a.boarA%rQt]cainA.d/ul]incidenTA#lT^e_g`A`i<i{u`ul/onel|e|ul_rate#mandA{ant~e?ul=t^bustibil^entariile^is_tetul^oarAEpaniaJe*i|i`raTie_etiTie4Nlet=A{x;icat~A{ment_orTi<tA|ament+entul}t_usA;ter}ul$un`e5TicA|are{tATii|ate~ea#nStient{inTA?a$Tine$cediat`ntra}ez;rt=ul:urs/damnat:iTie)i>le|onat_uUc<A|torHe)re~a(iUs^ectat_xiune~a^ferinTA_irmA|at_lict%orm<tabil_runtA}at:uz^secinTe:ider*A*are?t`liu>l_tant`rui>ascA}esc}m*t~APt_a&ct=a|ez4NeazA4NinuA>mWa>TiXre*t=e)i_rA;act*ul`ibuie~tUol=a)ul:ul/versaTia+ie_ine{g|A=e|iVs2Tol^perOpac;i{i;ul/ie4Mi5MiGlor4Ml`A{ria>e5Nul)ui]rd3Nect(A:ea{nA^oanA$pRul<ui^tulOstA:a`t_ul&m<ul]vor`ulCrAciun=ul.avatAOeSte(re>a/a%dA:scAFt;urA|i3Id4MeGTi&a<i6Nm6TuUm_inTA=a;t/eazA/ier(ul:on{ul^mA/scGut3Kzi4MutOimA%a:e&i%inal>i>ul^tic{A$zA]ucea/d1Fu]ScA#Tit&ulDiPva]lc_ARare;tPoare=a_ri{le/turA<a2Im/inteEpAr(A=mWturiHa|Ti7MtRereViEva2TnoSteaHi)nTA~eFaSte*Ti>m`scA4Msc6Nut>A.plu^tor]rATA;at`enie3MQnd$aj&os;ulRt&A$ent/ge/iosPs_A%a%ul`ri/te&a/vA#tiaRe_i/remurDvQntVulEinteWle>or0IdA2TdeaOm[Qnsul1IaDTi2HcA2MiOn^a$iel$ny$s_at_eazA`z{i2Hr2Kt3LA3Na$e_le^or;eazA<z=iUia6TeVtA2Mu.vePid_s1De.SertEi/teaptA`pTi(t]Tin;e5TutDa^l_ul{ui/nPsupra
2JcQt^edat_mbrie3Ki_d;e4NsRzia(e{i^laraTia~e=t^orat.dicat.fect{e]geaba_t`e<le&ulPrabA2LjaEun]licioasA~e=s3Noc]misia^ocraTia^ult.ntistDoarece/camdatA$datAPparte^sebire=t#pASit:rtare/artamentul6Me^endentPinde^lin{A^ozit|ul^rimat^un`e:s#ranja|Ti=tHeazA)z^ekDs^chiSi(d|A7Ne>Ti}mHsWA|e<zi_operi~reYt:rie{s%urc|A}m=a*t=i^earA_n`at_ori:rt^fASurare3Nigur$pArTit4Jre/tinul_ui5Ll{A<e#talii=le{u$ectiv}ul_rminAOveni6Nt$iiRnUAUe3Mreme]zamAgire*t~A9Tor:stru^gustAtor^vAlui_oltarea}t[iamante^na/volul#cTionar?ul^k]etA.ferenTA*a`iTiVt)AWePicilWA=e`ultATi>ate]mensiune3NineaTA8Na2GnPTi;i^afarA_inte$colo^spre^te_otdeaunaRr5Le.recTia|eGt{A<or*ul]scuTia)e|i`rs=ul;t(Am<a)tPearA^pAreaHut:arA{e<i|Tia_erare:onibil~lA`ziTia?e|tiv%usPtanTA=a_rAm&acTieWtiv<t`ezi5Tug|A)e7TiVs|A2Tverse^orT{atCl2Me]uiCnA]a[oDamnA5Na5Me{iVlor3IrFe_mAUe]cEtorVe6Ti7TiHul^umente~le}ul2LiPlea^sprezece]lar5Ni]meniu=l/n%iSoarA?aUlor4Nul6LeVui#n^naDrPeSteViRa&mFsc3NiRTi%m:nTA(aFtPm_eaFiUt<or}ul]s^ar`ele;ul2KuA_sprezeceRzeciPa^gOvadA^edeSte;i(t%zi{le1NrOA3NguTVA{e{i2Nacu`laVui^gFAFa_iFosteKa%ul(eOeaptAVa3Npt5MateGul{ri>le]ogatRuri|le2Num4Mul{ui`ri|leNuOS^man<i{ul]blA_u2LcPA3Me%Ti_a%m3Ni]lap`ulPce_i`uri#minicA)a^neata6MvoastrA5Mzeu}l9Ne2JpA#r^APa%t`a$eazARreVa;i`os:ze2Ms!vDs[ylan0Fe[Sec_ul2Hti#uat1Ia[chilibrulFpAGa{jul{mentul`e(i]onomia2Tran-d#die]iTie]ucaTia=e]ward!fect`ele`ul]icient}e.ort`ul{rile-gal_e_itate]ipt.oist[h1Hi1Hl2Me^ctricA6Tonice^fanTii{t^na/v:i&i]ibera|Ti)t{eazA/minat^zabeth]len]veTia[mail#ily^siunea.ma]oTie`i!nergiaVe_vant`eazA]glez6NAHa]orm]tuziasmat1Tpisoadele&dul]uizat1Ira/Ti3Ni3Lm3Mu.ic.oare/u:l[senTial}A#peranto#t3Fe-taj%ul]han1Hu#roRpA[va#eniment~e~ele]idenTAVt^tA_a1Mxact/men(ul#celent>A%pTia=e/ursieOemplu/rciTii~le}u2KistA;aVt{u;e<nTaOperienTA?a{ment~tul;tPlic{AVa)Tie~i)t<i_odat`zia|e/resie]terior/raordinar~narA`tereStriRem0MfA#cQndPea;i&m`u3IutUA&e2KrA[Qn1MaTA3Ma#bricA<a2Jc3KA3Ie4MTi%book4Lm3Ji^tura$ultate?a.imos]liment$s_A:e2Mmilia6NeWi<i|le.ntastic~A:omA<e2Mpt:e;leFul<ui]rfuriile]scinant2MtA3Na#voare|a_rit|A.zA!bi[eTei]brA_uarie.deral2Kl^icitWAri_eEul_riDmeiGa5MeUle<or]ratAPeastrA*a_stre}lePiciTi(re>a6MtJA|e$mADteRle&or/iTA&a1HiDTi2Je3Kcare/r_be&inte_t:ul]gurA2Li$cA4Na_e;i/nTA`a;e6TleFdGcA2Nlm%e;leRul{uiDmOnal;A`ul/e^landa]r^e$mA%a2Lu3MlRe%ui.x]zic;A`a;e-lAcAri#oare<aPri`da&le.uent^ture1Noame3IrteDcPul5Tui_ri.losUeSteXi(ascAVscGi<Ti(m<ndHt)A|e]nduri.rTA%a&t:elePmA:a;t_e`azA4Tularul^te2Gst_A:ulDtbal{ul/o_grafia+e+i~ile!raTi&i^ierPnTa`ei%cez7NAJa`is7TcoRk`ieEte5Mle(ui^zA:e]ecvent/d2NicA_aPg:ider^pturA|a#ucte{le/moSi5MasAJe5Ms:useTeYa^nze<le-u]g/AEi_Ti_mFt.m/a4TTi%t;ul/eazA:z`i^ul]ncTia<e<ona?tKeazA~ze$dRul.rAEat`A^e^ia4Te_oasA&s$tunA(a<ii.sese{rA^tA0TgAleata#seSteHi%ascA4Nsc3Mi:TiFm4Lt`A]teSte:sc^i:t1NQnd%eSteJi`aHm{scA5NscRi5TTi&m`re5Mt:ul;ri=le#t$ul[abriel.lben<A#rA^a_j^d_A/y2Mta#urA.y]z3Te[eacA^mul^ntA&a]loasA:s.n^eraTieVl|A|e=ul`os^ial:uEul:nchiOorge.rmanVA<aVia=ei!heaTA`a]icesc:i`t^d^nion1Tibbs[loanTe/balA/nT^ria#umA%a_eUSti`am`le;sc-oalA:eOl$f]rdon[rAbeSti`sc_i`m5Tt$dinA(aPmadA#
abA/ce$de^nt$s:A/tis:uit|A$v_A_e_idA]eSeSte|i5NalA=aUli=le4Nit<A{ePa_cA^cia^en^g/le3Mu:tATi`ate}a^vA.i3LjA4Ni]oapA_sA:zA&nic}A3Nzav(AOup:ul{ui!unoi`ulOrAEa]sPt:ul.vern{atorulVul>ui,hA[Qns.rtia&e!abar2Li3LdeGTi/nA:aReUle]n/k^nah]os#rry$tA_a^vey]waii[eather2Li]len5TaOnry#y[itler[m#m[o.T^i:i/ul]bby.l]mosexual]ng]tArQreaVtEel&ul]ward[rAnit]anA]istos-uh0Ii1La#d^ul]n$uarie2Kr^ASi/bA:a$nAFa^tAOsAOtA2Mu1MdeeFa$i:le/ntificat<tate~ea]ioTiRt;ule[e2NSi:Ti%m%re{a4Nt.ftin{A{e2Ni]rTi3Mi^nii3Tt:a;re`tOsPe1Tgnorat[i]sus&e-legal]uzie-magina|Tia~e=t<e)a|z<i2Mediat^ns`A.pact^eriul^lic{A(at_or/ortanTA8MtLAYeFsibil/resia|e=onant~antA+at[namicul.cendiu^ident3Tlude;sivPredibil.dia`n:cA`a`iu_eniiRferent.el:ul]finit^luenTa^ormaTia?eLi?ile=t.giner]iTialPmA4Na:ii`le]secte3Tist6Tat^pector_iraTia~e|t/tanTA_rucTiuni{ment$ulA`a]teligenTA?TaYt~tA~te:nTionat~eazA~ez`s:res|aTiKntYtA~teXt~AWeazA=ul&ior*ul`naTional~onalAVet;viu&zis}A3NrA&mRa&Ti;re)a5Nt%e%iRu.util{e#ventat_rs^it`aTi}a}iVt[spASitor]teTPoria(e.us_e-t#alia{nA|aCubeSteVi_a4Msc$i_Ti:mRreVa;iiFt`AUaUoUul=e#lie.nie[van-zbucnitBjack_ie%son^ob]f#keOmes^ieOne.ponez)AGia.son]y[ean.ff_rey^uit.nant/ny.rry]ss_e_icaNim$my[oDacA%e]b^ul2NcPiPul:ri<leOe/y2Nhn%ny_son.i]nes]rdan2Ls/hNucAm_rie{i=le%tor|ulPa_TiRt#decAtor?ul;a(tA]les/ia_e2NmAtate}a]piterDr^at3Tiul^nal{ulEul]stin@karen^l#te^ie-elly.n^ny.vin[g[ilograme:metri.m]ng!m[ong-yle]otoMlAsAm3NaRTi4Mt[QnA3MgA1Fa]SEi.borator~ul#c^om/rimi|le/ul]dy2TmpA]nsatDpte&le_opul.rg_A_i/ry2Ns3NA$e#tinA`a]udA/raOyla1Je.Sinat]agA]cTia;e`i#e2NgAturAWa^alRt`A;ePeRa_ndA^i:i:le$ume#mn_e.neS/t.o]u]wis!i2NberUA`e`i`tATii(ate+a#ceu;l]der;ul]ft:ul]ly2NmbA4MaFi`i&le{or/itA`a{t`e^pede]ncoln/da^gurAEiSte|aVit*A%a%e#psA%aReSte`sc_iUt.re#saPtA%a]teratura;e]z1Koc^aTia:l`A/otenent?te~tul^ui`Ti`a{scAGeSte>iHsc`m;t4Ll`uiRri<le]gic`A^oditOndra2Kr^d]s]u/is]veSte{i^iFt&urA=a|i[t[uA3Nm]Qnd2MaETi3Lt4TA4Te]cas$rAm_QndRa;Ti`reaGt4NeazA5Nz(eVi4Ku&l5Mri7Mle}or/y2Hi.ke2Mme4La^iRi%nAGa;ileDnA3Na^eaPgFA%i;me=aRul3Mi%i.p/Ti^tFA;mRa&t%e/ul]x0GmA2LcarDnQnc6NAVeHi/uSi#r^cuS^ii_me{a_t`atA/turie|sit/ulOsurA`a;i]tase^uSAUa1LQineRi5Nle]nEA3NaPcAmRa;Ti5NreJa5Nt/drA`i{eUu-a2MSinA5LaUi<i<le]c]drid]estreDgazinWul^gie^ia_c_e2Fi^estate/l^muTA^or]jorUitateaDmA3Ka^eFiPi]nagerul/dat^ual.rTi^ca&t3JeRa%le/fA^garet_inea3Ni4Ma:eUi_le:na$k/o/te%ie;n%or<i_y3Jy2MsAPa_j^cA.tematicA?a_rial{e/t_hewOx^im`A!da-e2Ia3NrgA#ci%ul2Tdia%c;al=A=e(ment+te~tele~tul`ii{nA&ul_e%u;l{ui]g2Li]lanie3Le/odia<e#mbri<i&u/oria<e]nTine;onat^iu`l^nad]rciPe:le4Lu3Lg_Qnd4LeGTi&a{m5Lm4Mi/iTi:tGA`at3MsFi_ulDsaj;e&ul/e_ria]tal/odA`a`ePri_ou{l2Iu]xic1IiOScA`m`ri%a`TiUre|a`t^ti%o]ami2Nc3NAPhael_elleEi3Tkey^rofonul^uTaFl2Me/rcuriRe$zulDi#jlocVulOke#lA$e/iardeFoane&n_tar|A|e^ler]nA^TeaRi`i;leUt/cinos&unA=i3Ie^ge&a/istru}l$t4NeUa3NunatJA=e;e_sFt5Me.racol/easa^oSiRase:s;ul#siune)a/s/ter]tA]zeria{e-m]m[oS^tenit.alePrA%eRtAGe6Na#bil`A`ul2Md/A$alitate$el:rnAPul_ri]lly2Mment<an<eHul#ndial=A^edA/struDrPTiUi^ganPi^mQnt3Nt]schee_ova2NtivUe{leUul^oarele_cicletA~ta:r&ul-r-uScat]Ti2LlTiGme|a_umeSt
i7Jsc{i|TiWmWt>A3It4NA4Ke:or.nTi`i3McARa%eSte=i;ascA&sc%it{or$te`le<ui.rdar<A<eEi:m4Mt.t/A_m^aRt^e]zeu`lEicAGa[y0NnAscut-aS^pa^teUre|a/ul#Tional}A}itate_une{i2LibaFii]sol/ul]te^han^iv^urA&a<l|A=e`ii.vAPa^e_i[chen1Ie]InTelegere]aTaPgrA/pAratDbunUA`esc&iVe.cazuriEesar=A=e&itA^onceput]fericire>t~A.gat`iv^re:iRu]maipomenit^ernic#norocit?A?ul?ule.obiSnuit]poTi_ata:liticos_trivit;ul#rAbdare$egulA^vi_oasAUs]vastA<a^inovaTi*t9TA^oia5Je`le;tDwNi2LSteOcAieri3Ji4Mo5KdatA4Nun<a(ul$kDmAnui3Keni3Jic]na^gA%e/s.sip#vel&ul[oDStri2Mapte6Ma3LstrA6Me2Ji/embrie^i^le.pTiUi]rAPd$i^mAFal<A3Noc;oSi<asA(s&ul:i2Lstru]tA$a^ele2Ku3MA_zeciEaEl-r1Du]cleareOmAr`A5Nul3Mai3NeRSte<i4Lle_rar;e<le`oasA%sc^i_Ti_mRt;A#ntA%a0Eo[Tel[aie2Kmeni6LiHlorOrAPe_care`um]se^peTi|i[bTii_nGe{rea&ut#iSnuia>mWt>A3Ncei<ul=rile^ect{e{ivele.ligat.osiTi5NtVA]sedat_rvAVat!cazia;e#ean`ul|ui#helari*iEi4Mi_lor:ul#tombrieOup%A`m:a;Ti5NtVA_e:i1NdatA]ihnA`eSte}i{ascA{sc!f.erRA_eRi`mUt:tA&a]f#iTer{ul$cial-glindA{a1Kh[i1Mk#ay[liver_ia1Lm.enirea#oarAUePrRIFQt_i2Nul4Ne%ui[n]line#oare<a^ratA-oh-pTiune<i]erA_a;Tia=e|une~ea#inia5Te.ortunitateOreSte(i%ascA%scEi:Ti%m_reFtDt^sprezece/zeci-r2NA2Ma3MS:e`leFulVui]b.dinGe{a<le;ul/onat2Me^i/le/z_ul]ganizaTie}t2Li/bil$cQnd;t%are4LeFine4Num^entul^ginalPunde[travA-u#A/le[wen[xigenMpA]Sit.Tit]cAli<tEatUe{le/iiOdure{a`ile2Mi^anjen.lAria<e2NmQntVul*ui.puSA`a#r^AseSti{ascA<sc&iVt$Ti`le3NeaRreVa$inTi7Ni)lor&te|leEulRt.sAri(le^a_t/trAm&a{Ti(t&eazA<z|e=i[InANQineUa2KnA/a-a.Saportul^i2Nce:a/het<ul^ienTi{t=ul]ginA`a`iDhar`e&ul]i]latul^mA.nicA/taloni+i%ofi)i.pAOr$APcFA:a;re`t_ul/don3Je/fumulPi:ezRs`ul%u^k_er^lamentul/ola3Lte5Ma;ner}i>ul`r_icipA>at{ular;d{AOs3NA%re<a3Tageri^ionat_une|a^tile7Tle/ul2Nt^ra_ia;ck4Mu`lea&zeci$ulOulPzA.zA1FeDSte;le`rA:i`i.deapsA|a_psit]nny^sie3Gtru]reTi{i%che%te{le3NfectWAPicol;uloasA~seXsRoadA|aPmis<iunea<ul;tHe=Ti^nA3MsoanA)aJe*leUnal>A>e}itatea}ul.scuit3Lte#teRr^reacA&cVe7NreLa}i{iHut_u-hil!iaTA:a$n/rdAPtrA`a2Mc^A:turA^atEioareXle&rVul^nic^tat_urA.ele&a/pt`ulPrdGe(m<re>a5Lut|ARzi$sA_e/tre.lot]per3Ti.scinA{aPicAUa;i<le^tA:ol<ul#zza1NlAcea5Nre=a:intA4Nut(A{e^nuieSte{t/teSte)i&ascAUscRi;Ti`mGt{AOQng;A;QndUe{a{re;i%s2MacRA4Je:iEjAEn%etA<a{ei_ificat_ta{t;e<leFul{ui&ri)le^sA%tic/tA_a2NeacA3McFAm_Qnd4NaUTi;m`re|a5Lt4Ne4Ni#ictisit?oare+or^mbAUare{tEnFA_eOoaia&e/iiEuA:aUt]uSEs[oSeta^tal2JTiDartA`a;e$tA4Ie.d$ea/ul]et^zia;e;i.ftA_iTi5Nm]ker#liTiSti+i6NaHe)iVst}ul%ticA=a=e=os^onia]mpierii]na]por;ul|ui^ulaTia<r|eOrTi`le$c_ii^eclA/neSte%itPt:ocale`fel>ul_ugalia(hezA?a^umb{elul2Nsibil|A|e|itATi~ate?atea|ul$t:ul2It^enTial$riveSte|scHit>A]varA/eSti|leFsteJa<itOzA$a$e:le$iTia<e_tiv[rAbuSit^jitA<urA}iOQnzUul#actic=A^dA$fOeSedinteLele~eluiPT_iosRul&rile3Ja:jmA^cisFum^dA_at;u_ea^fAcut4TaceRer<A<aWt*A}e<i^gAteSte=sc(iTi|mJt*A^ia3TjudecATi^luat/miu{l^ocupat_t/sA:iune}aRupun>e|s`s^tinde^veni$zenTa|iVt|a>t%int|A.icep{i{ut3MetenWAJaWe}le7Ni>a}e8Ni}lor=os7Nul?ui/m_A;varA>a4Ma;r<ul:eSte=i`ascA;leUscFi;i`m5Mt4Mul3Kn:Si_T;esA=a;ul%cipal?A~a%d;AUe<m4Ns:trVe_zi/vat<AFeSte|i5Ta`liStea;sc_i&
Ti&nTa(dUre)a&t^zA_onier~i.oSti<i/aspAt>A{eteGtA(e/bA4Labil:e4MlemA7Ma7Me}i*le^cedurA&s<ul_urorul^duc{Tia<e&s<e|le{ul/fesionist<oarA+aJr}e>i~iKul~lui_it{at:und|A3TgnozaRram=are)ul`esePiect)ul^miTiUs<iune?ea9TileGt{e/poziTiaYeYi?ileFria{ei=tarul~te?tea6Ti)le<uWl_un<erea3Nst;esc`ia(e<i|le`ule^tecTia>e&ja{eazA=z>e^vine`zii_oacA`ca|re|t]udent[t[uScA`rie_a/ti;ul=e2KTinUA&e&iOblic{A{e<ul}ui2Ni^i^ul]lover2Nn$AEct;e{le&ul3Me%Ti%m^gA2Nr^APta`Ti&t2Ms^A]te4MTi4Ja;iGm;u4KmRreHa`i{leGnicXA*e>i3Lut]zzle,rAbdare|a]cealA#iDmQiRnUA5Ne<Ti(m3Mas]neascA_sc$i:TiFt`A.pit]sArit^pQndit%und=AJe}Ti}reHsJul>ri~ile<zi]tAcit2Ju/l_ui]zboaie5NiVul*ui_unare6Te^gQndit!Qd^A$eDnd%ulDsOu/l_ui.zi[aTional.chel`te#dio;ul]ftDhat;ul.nA^dyDpid;A/ort{atVul#r^e:ori]sA.ta%t#y3Tmond]zA/na[e]Tea_tA`a^ine;utOa^cTiePl%A_eRitate~a`zare)t]beccaDceRnt_pTionat/iproc^omand}at`pensA/unoSti(aSte|scAVsc>AtorXut_perat]d^uce{re.fer;i^lectA/uz;AUatOgeRle;ui/inA&a_unea$ret{A3LulAUa;iVle|or#laTia(e<i|le4Txez$e/igia{os]marcabil?lA.nunT{A(aWt<e<i.par;a(t`e3Lede:t;A`a{t^orter$rezintA^utaTiaOspect=A|aTi}t=ul_ins&rA{aTia%onsabil~ilA~ili?ilitateaPtaurant+tulFul^urse|le.tras]uSeSti;sc%i5Nt]vAdEedere:ni(t/in`A:stA{a.zervA{are7Tt$istA^olv<AmVa)t<e:nabil/ultat>e?le*ul[icardo$hard^k.dicUA`a{TiVt|A`e`i&ol]ma.o.sc_A:ul;ri]tm_ul-oSePieRiEu]agA^ta#bert^in^otOchiaUe/k2Jg^er.l/ul.mQnA;iaPaRn`e;tic;ul]ssPt]y.zCuSine]de_le]gAciuneRm^aRt]ndA]p/ePt]s$A^aPia^sell!yan0DsAOi]lbatic>e]nAtATii&ate*a;oasA}e(s2NptAmQnA8NaKi?i#rac`A`i`ul^bAtoare=ri?m/i%t$ut&at`e]tulFrat2KuNInt!QmbAtA#nEgeUle^i_i1La.bia_e]c#lAPa_riu=l_tA5Ta3Me^ly3Nut`Ari`are$vA`m_a5TTi`re|aUt:ez<e<iDm3Mi^my]ndviS7Tul.rA$ah/cinA{a$e_a/i#t^elit^ul2Ju[cApAm%aGt/ri`le$zut2Tandal/p:A%e:i^rA_aPun`e;ul#enA_aDhimbVA|m=ri~leHa)re?a7Nt(e(i{ul.oTi/atAUe{Ti<m/pRul/rulEs$t:t2Nrie`Ti`m%i&tor4Ms&A`eGoareYa<ri}le`ulFuOump&A;eUo;ulePrtUA`e$zAFaTi4Me`le1Ge]amAUnA4Ma/n3NrA4Ma]cTia`e^ole&ul|uiEret<A{arA(e7Tle(ulPundAVe%ritate~eaOmn_Atura:al<ul;t:e:ul]nator^inEs:ibil:ul$timent+e+ele~ul.parat|e$tembrie#rgent^ial:e%oasA|e5Ms^vesc_i`ciileWu*l`t]t$eDx/ual<A:l$y]zon&ul[f.Atuit.Qnt^rSi6NtJul.at%ul;ri.ert]inte]oarA^rAie1KigurGA5ManTA*a7TtA`e;i]mT:ea<m4Mi;Ti`m5Nt_ul^bol/on^paticRlA`e5Nu3Mt:AFeDncer<A6TitateaPe3Lgur6MAHaVi|i6Nul^ucidA|ere<sOstem{eleHul}ui.teEuaTiaWe|i`t[lAbiciune~ea;tOab%A_e_i/vAOujbAUa-mith!oT3MiaRe&i_i3Nul&uiOareUle(ui_tA;a]cial{A{e_etATii<ate?a]ftware.l/daTi=i&t^uTia(eOmn_ul]phie]rA3Na.s^eSte_sc^i_reaFt^ul!pAl_a&t]aTialA&u{l$lA/nia`olA=a^rgeRt`AEte5NleDecial)A=e;i%tacol?ul^li^ncer3Mr:AUmRanTA=a_iaHt=A&e;i]ion/rit<ulEtal<ul#ort2Mre^ijin|ul2Kui3Kn4NA:Qnd4JeGTiUa<i<m{uUm3Is%e[t2NAPm^pQne{ulPtea{m.Qnd_gAUaDaETiUa&e^bilA(it3Ki^n^rFe&a3Nt_e&le<or:ul<ui3NuDea$le`le^phen$veOiclA`e/l4Tou{l:ul/nge:s]omac{ul/p]rAduiesc%in<A)tateHe<i_luceSte|itor:zi<i{le^Qnge&sPadAUa^eet/icAUat;t{A:gA{t#udenTi>i(t|A7Tul:iaVt(zAUez=e=i`ile;u<l/pid{A-ua2Lb$iect)ul^sol#cEces(ulOd2Te^dia.ferA;i{nTa(t^icienTiKt?A?e^lA%etVul}ui^ragerie.gerat;ez4Tstie]mA^aDn3NA_mPa_Ti4Nt$e_t&ulPi3Gt4LeTi5Km#pA_ra{TiHt)A/aPer&i;mark
et$ort(a/rafaTA}a;veghere(ieTui?uit_emA]rd/ori<i{le^prinde~reWs}AVzA/sA_a_e2Ms/Tin(e/an^pecTi<t|at|ulOtAPe[ydney,tAcere(a$ut2Ni^aRt2Ju[Qmpit2NnArUA`ul.rfA3Lziu1JaOTi.bArA`a/lou{lDci.i$e2Lle:nt<at2Mre]staturA2MtA4LlGui3NaEoeba]xa^e$i_ul.ylor1Ge.amFA/tru.d^dy]hnic{A:ologia]lecomandA:foane~le6Nn|at7NulFvizor+ulOm/a$eRle^i/peratura9Trile_lu_orar]ndinTa$is^siunea.oria`e]rapie$en;ul/ibil|A_toriul$men{ulRinVA)mHa|Ti7Mt}A<e<i^ry#st_e%ul]xas/t_e4Tul[hatDe#omas-icAlos|ul~e]m^bre/id3Jp4Kul(ui2Ine:reUi2Mp/ii3Nul`e_ri2Ttlul]u-o2KTiFi#aletA^mnA;a3KtA4Je]by2Mcmai]dd]ki/yo2Tlera2Gm$my]ne$y2Tp^it#rt2Jt$al`A;itateEdeauna3NuSi4Kl-rAdatEi%ascAReSteWi5Nsc%mRt2TadiTiile:uc<e|Ti=reLa}i{i`s^fic<ul$g:AFe;Ti`die:i^ndafiri:sformA+at~e`mit}e`port~ulEs/tament;t_eazA2Te3NabA5Na%cA%z`A3Jbui6Ma6He6Mt`ri=lePc_Atoare4Ne`Ti&m5TreRi4Lut6NA{e(ul3Ki%a:lea_sprezeceRzeciPnFul`rile^ptat/zeSte=i&sc:iGt]ibul;nal^cou<l^er/miTi5Ns&t<AHe|mPst;A`eTe]uc^pA_ele:ul1Iu]r/A^cA_a^mA^nat_eu:ul3Tul2Nturor!v[ylerBuSA2Na]i/leOoarA3Mr]urat:el:inTA-au[ciSi/d:AFe;rea/gaS<ul3Ns_A^ziChCiTi]mit`oare(r2Nt3NA%m3NaRTi:m4Mt3LeCl.ei_ul#timA5NaUele&iiGul!m]Ar#anRARe]brA_a_elAVa]eri]orului]ple%ut1Fn2LaOchiul=e|ui]dA3IeFva2Mei3Nle3Nori]ghiile]ic_A^formA3Ni^tate=aRe/vers=itate?atea)ul~uiOor]sprezece]tDu3Mi3Ll!rASte;iEscOQt:A#a]c$A^a_Ti%t^i]eche{a;i<le^z#genTA;t.i^aS`A^le2MmA:reSte>i{ascA<sc`i{Ti{m{re(tRtoareYa?le{r|iiWulEa%re%t$eRazA:le4Tz`e`i.s^ul-scat-til_e0IvA2Kd.i]l]rsat^ul]zuse4Kt-QnAtoare$d:ARut$tRul$zare]rf%ul3NstAGa1Ha.caRnTA{a2NdA]labil^e/iza$oare|a:reazA`ii^uri]mpir.n]porul#rAEa]s^e:le]za[eSnicie$ti`le2NTiDche;a4Ni;ul^in;ii;ul|uiOdeFTi4Ma4MmFre<a4TtA]gas2Ki]nea3MiFTi%m_nd4Kt^usDrde$ific)A}m|aTi*t|i_i^suri/zi]sel`APt:e&a2Lzi!i2LaTA4Ka^tA#ctimA<e|i|le:or<ia=e8Ti#deo.e/TiGi;le^na2Mi3NtoareUrVul2Mn3MAEa^ce`ntPde`cA{at`m3Le%ri3MoRvat|A$ul/zi]oarA/lenTA=a{t5Tt]rusulOs$at/e%le:z$ul#tezA#u2Tzavi$itAUaVt`eazA(z|e_une[lad-oStriDastrAVe]cabularul$eRa^i2IiPa:iFm_uEe^nTA`ei]luntar2Km]psea2KrPbA4Na_e5MSte7Mi&a<m6NscA{u5Lsc4MiGTi5Nm&nd5Mt{orOstru]t^a:t^eze^ul]uA-rAjitoare2TajA2NeTi3Ja4Iu3JiEm4NeGa:uri|le3Mo4MdatAEun`ul.oia`i&m2Lut@walker/ter#shington]yne[eb#ekend]st[hisky]oa!ill:iam^son!ow,yanni[eah.ni1ToDrk#uMzApadAUa^ezii.u[QmbeSte|i;t{ul%it!ahAr!boarA$r_i:ul.ura&t1Nece^i]elandA]i.ro]u[gQrie#omot{os<ul1Ki#ar_e`le:ulDcEe_Ti_a_m3Ni]d^ul2Mle%iFle/nic#ri2Ms2LuaNonA$a]ologicA]ri-vonuri"""
DATA_EN = """0Da!ah-bandoned#ility2Mle2HoutPveOroad.sence;tEolutely-ccentFpt(ed%ss3NidentPordingRunt$usedDrossDt/ed$ingRon<s/or/ress3Mually!damOd/edPress.mireRt;ted.ult.vance&tageEice%sed-ffair<sPord2Mraid$ica2KterGnoon1Kgain5Mst2NePnt/s2MoDreeUd;ment1Nh2Nead-im2Nr/planeRort-l.an$rm.cohol#ex.ice/en3Nve2HlPowUed2Mmost2Mone4Ng2LreadyEight2MsoOthough2Kways1JmOazing.bulanceDericaJn*sOong$unt.y1In#cient2Fd/y#gel%r3NryOimalVs.n/a/oying2Lother2Mswer(ed(s.xious2Jy3Nbody3Mmore3Mone3Kthing3NwayFhereNpartUmentOologize#parently$ear<ance<ed(s$lauseRe&s_ication:y$ointmentPreciate:oach.ril1GrePaEn't.gue%mentOm/edPsPy2Kound.ranged$estVedPiveHd;ingDt/hur$icle%st1Hs#hamed#ide2Lk3LedEing/sDleepDs$hole$istant$ume1HtDe.mosphereOtack<ed/empt%ndGtion/itude/orney/ractive!udienceOnt#stralia.thority!vailable.erage#oid-w#ake$re3Ky#esome#ful-ye,babe/ies3My2Jck:ground2Ld$lyDg/s.lanceEl%s#nd/gEkOr$ely/king#seRball%d:ment/ically/ketballPtard#th%roomPtle1GeOachPr:dEt:ing3MutifulUyDcame4Juse3Nome(s&ing2Md$room2Ien/pingEr2Kfore#gEanPinUning;s.have&ior3Nind2Ling;s2LlieveWd)sPl$ong(s%w/tOn/ch.sideVs3LtDt3Kter3MweenOyond-ibleOcycle2LgPger&st#keDll:ion:s%yOrdRs$thGday2MtEch$e/ter1NlackPme.eeding:p/ss$w#ind.ock3Nod&yPw:ingDueNoardEtOb/by.dies3Ny#mb.ne:s2Lok4Ns/ts.rder$ed$ingEn$row<ed2Nss3Mton2LthRerPtle%om2Nught/nd.w/lDx/es2LyPfriend3NsNrain;s/nd$ve/zilOead4NkGfast&ing;s%th(e(ing.ian/deRge$ght$lliant3Mng&ing&s$tish.o3NkeGn3MtherWs3NughtPwn.ush-ucksOddyOildGingRt#llet%shit#nch#ried$n%ed%ing/st2Ns/h3Miness3Ny2Ht/t:er%on2My$ing1IyDe,cabOke.lifornia3Kl4LedFingRsEm2LmeFra$p:aign2Gn3K't/ada/cel&r/dy3Mnot#pable$italEtain2KrPd%s3Le%er4NfulWly%s^l$riedFy&ingPs2Mse:sPh/t%le2Nt3Nch$s2NughtEse&d-elebratePl#nter:ral%ury.remonyEtainJly-hainRr;man$llenge/mpagne3Mnce<s4MgeHd(s&ing$racterRge<d<s:ity:lesUie:ming/se/t#eap:ting3Nck&ed;ing$ering&s%se/f/ss:t.icagoRkenPef3Mld&hood5MrenPnaRese#ocolateEicePose$se;n#ris&t<ianHmasDucklesErch-igarette.rcle:umstances.ties:zens3My.vil-laim3Nss;es;roomDean;ed&ing4Nr;edUly;s$ver#ient/mate:b;ed#ock3NseGd&r;s;t:ingEthes/udsDub!oach/stPt#de2Nffee2Mld/lect=ionGge$onelRr2Ime4Ms$fortable3Ling$mand)er:ent:it(ted>eRon%unity/panies6Ny;red:etition:lain>ingUeteKly<x&icatedFuter>s.ncernWedVt$dition?s/ference;ss:idence%used$gratulations/nected=ionPsider*ed>ing:tructionPtact:estRinue>d*s%ractGolPversation%ince*dOok:ed:ies&ng3Nl#pPs$yOrnerPrect.sEt:s.uch3Jld;'ve5Mn't/ncilRt;ing&ries6My3Nple$rage4MseRt$sinOverUed.w/ard-rack$p/sh3Nzy#eam%te(d;ure$dit$w#iedPme%inal/sisOoss;edPwd.uel/shDyEing!ultureOp.re/ious/rent.stomer>s2NtPe/ting,da2MdEdy.ily#mage3Nn.nEce%ingPgerHous/iel$nyOreEk:nessPling#taEe$ing2Nughter.vePid.wn2Ky3Ls!e2Mad3Nl:ing3Nr3Mth.bt.centPide6NdFsion>sDep%ly.feat:nd;sePinitely.gree<s#licious:ver.mand]nied/yOpartment$ends/ressed.scribe/ert&ve=s/ign%rePk/perate:ite/tiny%roy)ed.tail(sPective:rmined.veloped=ment/ice%l-iamond/ry#ck$tionary2Id3Kn't2Me3Nd/s/tOfference8Mt4Nicult?y.g2Nnner.rect<ion<ly(orPty.sappear+ed(ointed:ster$coveredRuss=ed=ion$ease/gusting/h%es$tance:rict#vorce=d-na1Go.c3M
tor(s/uments2Kes4Ln't2MgPs.in4Kg.ll:arHs2In't3Le2Lor%s#ubleFt2Jwn:stairs.zen!r.agon$nk$w:ingDeam;ed;ingUsEssUed/w2MinkGing&s3NveUr;sFingDopRped$ve#ug%sEnk#y-uckOdeOe#mb2Nring.stOtyNying0Meach#rPlier4Ny/n$s3Nth;quake.se$ierRly$t3My2LtPenEing$s-conomic<y-d.die.ge#ucation!ffect<s$ort<s!ggPsNhCight2Nther-lected;ion;ric>ity/vator2Lse-mail.barrassed?ing#ergency#ily.ma.otional.pire/loyeesPty1Mnd$ed$s#emiesRyPrgy.gaged$ine$land4MishDjoy&ed;ing2Lough#ter&edPire<ly/rance.vironment!qual/ipment!r.icNscape(dOpecially%ranto.tateNurope<an-ve3Kn4Ning%t;s&ually3Kr4Ky5Mbody5Lone5KthingUwhereOidencePl-xact5MlyPm%inationRpleOcellentFpt/hangePited&ing3Nuse#ercise.hausted#ist;enceDpectVed(ingRnsiveFrience?ed<ment;tElain=ed&nation:osion/ress=ion#tra;ordinary%emelyCye3Ms0Mface:s3Nt%ory%s#ilRed%urePr:ly$th#keDll%en%ing:s/se#miliar<es5LyEous#n/cy$tastic2Mr$m.shion3NtRerOt$e3Kher<'sDultOvorGite-biCear.d#ed3Ll4NingWsRsEt2Nll%ow3Nt#male.nce.stival.ver2MwNield.fteen:y2NghtUingEureVd#le:s$l%edEm:sOnal5Nly:ncial3Kd%ing%s3Le$ger(sEish6Ned2NreRd$m3KstDsh%ingOt2MveOx$ed-lag$t.ewOightDoor$werHsOy$ing!ocus#lksElowVedVing.nd2ModEl:ishPt%ball2GrPce&d&sPeign%stRver3MgetFiveFot(tenPm:er$tune:yEward#ught3Lnd3Nr:th.xNranceRk.eak/d3Ne%dom3MnchPsh#iday3Lend(ly6Ls)hip/ghtened2Iom3Nnt/zen#uit1Muck:ed%in6Ng2Nll:y2Mn/eral3Nny.rniturePtherDture,gain2MmeRs.ng.rage/bagePdenOs$ps#te2Mve#yCeneral=ly<tion;ous$ius$tlemanWenOorgeDrmanVy2Ht3Ns3Lting!host;s-iantOft2LrlFfriend4Ns2JveFnRsEing1NladEssUes.oves1Ho#al2Ld$damn/s2Nes.in4IgOld:en$f2Mne3Kna2IodFbye:ness:s.rgeous.sh2It3NtaRenDvernment<or!rab:bed$ce/de$ndUfather&ma(other;pa:t;ed/ss/teful/ve/y2Keat;er(st/ekFnPw.oaning&sPundFpPw%ing%n#unting&s-uarantee%d;s2Mess%t&s.idePlty$tar2Nn$s:hot2Ly3Ls-ymBha#bit2Id$n't2Nir2NlfPl2Mnd%edFle4Ms&omeEg%ing2Mppen6LedHingHsRiness4Ly2LrdRerRly$m$ry2IsPn'tOt3Ne:d%s2Gve4Nn't3Ming1FeO'd$ll3Ls2Mad:ache:ed:ing%sElth(y3Lr4LdRing4Mt;sPt$ven:ilyRy.hOld/en3Ml4Mo3JpFed:fulRing:s#nry2Hr3He:'s$oEself2Ky1Mi.d$denPePing2Mgh%er:ly#ll2Hm3Mself.re%d2HsEtory2Nt^tingCmm-o2MldRingPe$iday$y2KmeRworkDnest(lyFyPor:ur.ok2Mpe:d:sPing.rn$ribleEse&s2Nspital2NtEel2Nur4Ms3Kse&s2HwPever-ugPe2Mh2Nman&sDndred=s$gFry/t:ing2Nrry3Nt%s2Nsband0Ci1M'd2Lll2Im2LveCce1LdeaRsOiot1Hf-gnoreNll/egal$ness-mage:inationVeOmediately.portance8MtFssible$ressed=ion>ve:ove1Fn.cident/luding/ome/rease&dible#deed:pendent$ia;n:stinct:vidual/ustry.fluenceEormation#juredOnocent.sane3Nide/pectorEtead:ructions$urance.telligence?nt%nd<ed;tionRrestKedKing&national(et&view3Ko$roduce?d.vented%stigation/itation&eVdPolved-ron1EsOland2Ln't#sue;s1Et#'ll3Js#alian%y2MsPelfBjack%et%sonOil.ke.m$esOne2Npan5Nese.son!ealous.ff]nny.rk/ryDsusNim$my1Lob$sOe2Nhn%nyDin:edOke:s/ing.nes#urney#yNudge#ice.lyOmp%ed.ne/ior.ry2Hst%iceZkate1Keep%ingRs.lly#nDpt.vinDyPs!ick%ed2NdPding3Ns2Mll4MedUrRing.m2Lnd:a:ness%sEg:domDss%ed:ingOtchen-nees3LwOife#ock;ed;ing3Gw%ingRledge4Nn4Ms-yotoZla.b#ckOdies3Ny#idOkeDnd3NguageXsDrge;r;st/ry2Kst2Lte%ly4Mr:st^inOugh&edGingGsUter/raDw/sPyerOy.zyNead%er:ing:s3NrnGedUing3Nst3
KveUs4Ning.cture#d#e2LftOg$alPs#nd2Nss%on<s2It3M's3NterVs%ingOvel!iar.bertyPrary#cense2NePdPs$utenant2Kfe$t2Nght;ning&s2HkeFdRly4Ns2Nne%s^k.on.ps.saEt4Len(edVing.terally3Jtle2LveFd4Ns3Ning-oad/nOcal:ted;ionPkRedOndon$ely3Kg4Ner2Jok4Med4Ling4Ls$seDrd2Nse:rPing$s3Mt2KtPs#ud2JveFdRly:rFs/ingOw$er!tCuckFy/y2NnchCyingBmaDchineDd$am;e3Ke#gazinePic#ilPn#jestyPor2Jke4Ms3Ming#le#ma2Jn$age(dVr/ner<s3Ky#p.rch$iaPkRet:sPriage5MedFy/tin3Jy4N's.ssEterOtch$e:rial/h:ematics/t4Mer(s#x2Ky3Lbe$or1Fe#al:s3KnRing4NsFtPt.dia%calUine2Met4Ning#mber(s/oriesUy2Mn/talRion=ed.rcy/ryOssFage2Mt/al/ers/hod.xicoNichaelDddle$night2LghtOkeOles$itaryEkElion=s2Lnd:s3Ne$ister3Nute6Ms.racle$ror.serable3MsFedFing&on3Ntake=nWs:er.xed!m#m-obile#del%rn2Mm3Nent<s$myOnday3Key/key$ster3Nth5Ns#odPn2Jre3Lning2Lst:ly2LtherOuntain*s/seEth2MveFd:ment:s3NieUsFng1MrOs1JuchOmDrder(ed=r#seum3Mic3Kt1Gy2Mself/tery,nah#ked2LmeRdRs.ncy#rrator.sty#tion(al%vePural=lyUeCear:byRlyOcessary$k2JedFed4Ns.gative.ighbor*hood>sPtherOrvous2Jver2Kw3NsRpaper?s2Lxt1Lice$k2Kght;sOne1Go2MbodyOiseDne$sense.on.peOrPmal<lyPthOse2Gt$e:s3KhingPiceVd#vel2Iw/adays$here-uclear2Mmber(s#rse#tsMo'clock-bey.ject#viousWly-ccasion/urred#ean-dd1Ef2JfEer&ed3MiceVr=s;ial2Mten1Ih.hNil1Lk2Jay1KldEer1Gn2Lce2He$'sEs.line3Jy#toNoh1MpenRed%ing:s$rationDinionOportunity:site1Jr.ange2Nder&ed&s/inary#iginal-saka1Kther5Ns&wiseNught2Jr$sRelves2Ht3Nside/ta1Jver!wOe2Ln$er/sZpack:age_ed#geDidEn:ful%t&edUing$r.l/ace/e.nic/ting%s.paEer&s#rdon3MentsPisEk:ed:ing3Mt%icular?rly;es%ner%s4MyDssFed;ngers:ing;on:port3Nt#th/ienceVt=sOul2My$ingCeace#n/cil/ny2Jople#r/centEfect)ly:ormanceEhaps$iod$mission3MsonVal>ity>ly.teRr1Mhone$to&s.ysicalNiano2NckRed:ing/nic3NtureWs.eEce&s.g.lls/ot.nk.pe.ss#ty#zza1LlaceUs/in3MnFeUt%nedUingRs%t;s/stic/te3LyRed&r<s4MingRs.easant5Je(dUurePnty#us!ocket.em/t2Nint&s/son2Mlice(man;y:te&ical)s#ol3Nr#pPular(tionOsition<ve/sibility6Nle)yPt.t/atoes.unds/red2Nwer&ful;sNractice$y.eciousPfer$gnant$pareWd/senceHtFidentRs&ure$tend=ed4Mty/vent:iousDice&s/de/est$me$nce(ssPson<er>sPvate$ze2Mobably4Llem7Ns$cess/duct=ion=s$fessionalWor$gram&essPject3NmiseWd=s$of/per<ly(ty%osalPtect=ionEudPve:ideCublicDllRed:ing.nch/ished<ment.rePpose/seOsh:ed2Kt/sPting,quality/rterOeen3Mstion8NsDickGlyEet;lyEt4Me,rabbitOce/helDdio2Nin%ing:sPse&d2Nn/g:e.re:ly.t$e3Nher#yNeachUed3MdFing4My3Ml%ityUzeWd4Jly3Nson<able(s.ceiveWd:ntVly$ognize?d:mmendRrd(s2Nd.fuse(d#gret/ular.latedUionshipRx$ease=d/igion=us#main<ed<s3Lember>ed$ind<s/ove<d#nt.pair$eat/lyEort<ed<s/utation#quest_ires.scue$earchPpect:onse)ibilityYle3NtFaurantPult(sDturnVed.venge/olution]ward!iceEh%ardOdEe$iculous:ng2Ight&sDng%ing%s#sePkDver1Noad.b/bed$ertOck:s.ger#le$l.mantic$e#of3Lm:s.pe#se:s#ughEnd.w.yal!ude.in%edOleRs.mor2Mn3Nning$s.sh/sia(n-yanBsad2Nfe%ty2JidOke.lad%ry/e:s$tOm3Le.n/d%wich/g/ta#rahDt$isfied$urday2NveRd/ing2Lw2Jy3Ming3Ms-careGd:yOene#hedule3LoolOience;tific=sts.ore/tt.reamVing<s:en:w;edCeaPrch<ing$sonEt:s2Mcond(s3Nret(ary(s/tion^ureUity2IeEing/k3NmFed4Ms3Ln$s.ldom$f:ishEl%ing2Nnd:ing/ior3Nse:
itive3NtFence*s.parate#rgeant/ies4NousWly$ve;dRice=s2Nt/ting%le<dDvenFralDx/ual/y-hadow$ke3Nll$me$pePre%p2He3N's/ep/riff#h.iftEp:sPrt3Mt.ock;ed/eFsEot&ingEpRpingErt3Nt:s3JuldV've(erHn't%ting3LwRed&r%ing:n%s2Nut#y1Nick2Nde:sDghsRtEn:al%ed:s#lence&t$ly/ver#milar/onEpleUy.n3LceEg%erRingFle/k2Lr2Mster(s2Mt/eEtingEuation2NxOze-killsPnOy1MleepGing;yPpt.ightly/p:pedOowRly1Nmall;erPrtOell;sOile;d:ing$thOokeRing-nakeDow1Ho#ccer$ial%ety/ks#ftOld%ierWs/id$utionPve;d2Jme4Nbody:day%how4Lone4Jthing;ime8NsFwhere2Ln3Ng%s/s2Lon%er2KrryEtOul3Nnd;edGs$p/rcePthCpace/inPnish$re2Leak&er5NingUsEcial;esPech%d/llEnd;ingFt#irit#litOoke&n/rt&sPt#readPing.y!quare!taff$ge$irs3NndGing&sPr:ed:ingRs4Mt5MedUing&sEte&mentGs4Nion3LyRedRing:s#eal;ingEp:ped:s$veOick3Kll.ockPleUn$machPnePod3KpFped:sEreRiesRm4MyDraightFnge)r3Neet(s%ngth:ss$ikeEong<er/uckOuckEdent7Ns%ied<s;o4NyUing3Nff3Npid#yleNubject#cceed=edUss)ful3Lh/k#ddenVly.e#ffer<ed(ingOgarPgest)ed=ion#icidePt:caseDmmerDnPday#per;market/per:lies;yRortGse7Nd2Kre%ly/face$geryEpriseKd/rounded$vive=d.san$pect:iciousNwear:t;erEet&heart;ieDimRming/tch#ordCystem0Ntable.il2Jke4NnFs3Ming.lent3KkFed4Ling%sPl:er#pe#rget#skPte;s#toebaOught.x$iCeaEch5Ner=s&ing3Nm/rRs.chnology.dOethOlephoneRvision3Il4Ning%s.mper<ature:le2Nn/dPnis.rm%sErible=yDst:s#xt!h2Jan4Kk5Ls3Et4L's2Ce$ater3Kir3JmRselves3Jn$ory3Hre5M's;fore3Kse3Hy:'llGre.ick$ef/n4Kg5Ks4Ik5MingGsPrd:styRty3Fs.omas3Kse/u4Ngh6Kt)sRsand*s.reat<ened4KeRw$oat4Lugh=outFw;ing;n.under/s.yNicket(sOe/d.ger$htDll.m3Ie4Ms#ny.p2Nred:s1Do.ast2Kday;'s2Lgether#iletOkyo2Kld2Fm3M's/my3Lorrow#ngue3Might$y2Jo3LkDp#talUlyDuch;edPgh/r#ward(s/er3Mn.y!rack$dePffic3Nin;ed&ing$nslate>ion/p:ped/shPvel<ing.easure%t&ed;mentEeRs#ial$ck3Med:sEp.oops3MubleOuck3Me$ly3Nst;ed3Mth2Ly3Ling-uesday.rkey3Mn4Ned%ingRs1Nv-welvePntyOice2JoNype,ugh#ly1Lh1Nm#brella-nable.believableDcle^omfortable2Mder5Lstand?dingWood#fortunately.happy.iform$on/que/tFed$verseWityOless/ikely2Mtil.usual1HpOonOset$tairs-rgent1Is2Le3Ld$ful$less/sDing#ualGlyMvacation.in.lley/uable%e#n.rious-egetables.hicle.rsion3Iy!ictim<s:oryOdeoOewOllage.olence<t.sionFtUed;ingCoice;s#te0KwaitRed4MingDke2MlkFedFing:sEl%et:s/ter2Nnna3Ht4Led:ing4Ls2NrPm/n:ed:ing2GsPh:ed:ing=ton3Nn'tPte;d:ing2MtchUedGing3Mer.ve:s2JyPs1Fe.'d3Nll3MreEve#ak/lth$pon(sErFing:sEther.bsiteDdding2MekRendFsOightPrd2Nlcome3Il2Knt2Ire%n't#st#t1Fhat4M's4Never.eel3InRever3Jre&'s;verEther2Lich3Lle3Nte2IoP'sEa$ever3MlePm/oEse2Iy!ide2Mfe#ld3Hl:iamUng2NnPdFow(sEe/gs/ner:ing/sPter.sdom$e3Mh:es.tch3GhRin4Lout$ness!oke.lf2Lman3Nen2Ln3M't3Nder(edHful(ing#od%s2Mrd4Ns/e3Jk4Ned&rs4Ming4Ns3LldEried<s4My;ingEseRtEth2Iuld;'ve5Nn't/nd;edDw1Nrite&r;sFingFten2LongEte,yard1Ieah3Lr4Ks.lling%ow#n#p2Js3Mterday2Lt!oDrk2DuE'd4Nll4Kre4Nve3MngUer3Gr4Ns5Lelf=ves$th,zero-oo"""
PAIRS = """!(E%[ !)CbT !*DbT !.@.] !3@NxEbT !@C.] !JE&CF:RF<IGCDGc<GbRG9WHWwH6[IP$I%SK/?KStL/hLWr !bC.] !eB.] $H>J: %0A%hBEhJ'lJ&DKXd %>>-] %A>-] %CA-] %M@-] %N>-] %hA<9CZ<G8oI7|J$gKbA %jB-] %mB.] &$?V` &CD/&D/VDQwE6ZFWv &RFSt 'bG.] 'zA.] ){?`0?;AG$1I:, )|@.] *'A.] **G@2 *iI.] *p=4{ +TD$w ,dF.] -HF.]FXh -ID6[DQ, -]B^REbTJ&D .V@!' .]AV: /'CV` /H>V` /PD&D /pFK[FbRGCCHbA /q=E@ /{=/p /~>E@ 0rCbT 1u>.] 3K=-] 3L>-] 3P=-] 3`>-] 3a=-] 3nD^:EXcF)GFE3H,WII~IbS 3~EbA 4{B/pGH7G^:Hc<IE%JdoJ4mJ6ZJHPJ/VJE2JVDKbfK?RKWvL:vL@fMMt 6=AW+ 6E@V` 6]B/iG/VG>lH%SH:Q 6s?VV 7DE.] 8CC!' 8sH.] 9:@%hFbT 9`GY! 9mBaIH.]J6OJCDJK]JY!MXd 9|A.] :U@*i :V?*i :WA*iE:QE.] :fDV` ;%B.] ;CD.] ;DC6Z ;gD.] ;hBVV <PBVV <aC.] =oA!' ?B?!' AwA!' BXD$}EK]G`pHbSH0mH/WI>8I%RJVdJ(BK8H CDA9W CvD!' D=A.] DAE.] DG?^R DQC&D DgFbTG%tH'l D~CbT E3FV` E@BH1 EHDV` EhFbT Fb@%h G4F.] GYBV` H1F.] H8BV` HsEbT IE>4{ IL?Dh In?$K J$B9mC?HDFbDDgIa/JBSKZHL%[ J:CV:FMsFE2FCCFQwF4lGI|G/VGNRGX~G:vGVDGK[H%RH`+I@TIc<I,VI;LI=+IE%I8zIDPIQ,J/&JY:J;eJEGJ7lK'/Ka7KaCLQ9 JpC.] K:C!' KwBCC M%@-] MQA/FA^REEiF^:GVDHDPI:QJ4m M]@%hA-]D^: M}ESt Nx?V:EHQFdpF0y ON?V:D4[ P(A.] P1?V: Q-BV` Q<?4l QQ?/h RI@V` RQ?VV S4?V:E$1 SdA-] T~D.] UO>Qx Uw?V: V$@!' V:CDgD;CD:VFbAHcRJA*L]@ VEA&D WqCbTD$0D'IDa-F]{GW?I.; Xa>-] Y>AV` YZDV` YoA,, Z.A/V Z2?-] Z5?-] Z<>-] [-B<J []G.]JY! ]4A.] ]HAVV ]QAUwFbT ^!B`, ^??!' ^JBc= ^R@%hAJ$EV:EbTL.1 `0=V: `2=V: `3=V: aII8HIMRISt bA@Uw bRB.] bT@;AD$1EOHFBSG38G%[ d$D4[Ea/EBSF[UGb3 d/E.]E%[ d3C<J d7B<J d9C<J dJ>V:E.] dK>V:C.] dL>V:D.] dYD.] e?EV`"""
PAIRS_EN = """!!D3lD.[D3OE5~E,tFAvF3^F.wF41F$vG%%GBaG&IGBxG$-G%?G)?G-nH9$H=)H'1H6&H2^H*>H$JH1oHB-H57H&pH5#HCKH5,H3/H(ZH*CH?OH'iI7zI({I5>I&[ !&=@R !'B1SC?pC@.CBmC@Z !2=@R !5>?r !M?6O !R??r !W>C; !jA?rC6OD)?D6(E7' !mA+r !o?C; !uB67 !~C0OC6^E!1 ##B4BF?w #2B5BC3`C6z #5B+? #6B!'C+? #J@CwD67EAv #L?Cw #S@?rA/| #`A!!C/ZC=PCBgD0oD5TE8WE3^E,V #cA@Z #d@4RA4BB0- #l@?rC!jC0<D2{D6bE6(E;H $$A-s $+@@RC0< $DB!!D!&D/|E2dE$+E/KF&NF*K $M@6OA/Z $N?!! $SEB+ $X>@R $c@?p $oB-n $q@?m %?A1N %E?1! %N?!! &+A0fB/Z &/@!! &1@?rD0. &6A4R &;@@R &?ACwC*<C$DD=aE;dE/u &@C$cC$DE!L &L?6O 'oA@RB$+C/|D0< (RACwB67B$D (Z>6O ({>6O )C?C; )J>@R )w?CwB@ZB67 )xB2MBB6C/W )}>$r *!?@R *<?CwB1SB?pD67D@.EC;E#6E=H *A@67A@Z *BA2MBB6B3@B/WC;g *JA2MBB6B/WC@(C3@E5tEALECVF-UF&LF,h *PA?r *q=@R *s>?r *w>6z +&?@R +J?6O +W@@RA5; +lA@2B0o +qB;j +r?)?B5C +z?Bm ,&>4R ,V@#`@-s ,h@3@ ,mA#g ,tA)@B5$ ,z>7$ -(A7$ -3@@L -7ACmB5$ -NA?rA!!C4RD01DC~E/{E@9FAcG*% -R@2[ -^>@R -aA7$ -s@?rD01D/| -t>6O -{?6O .0@4RB4B .<B!!C7$DA]D4?D$+E!oE:T .F@4RBA] .N@@RC7$C?yC0<DC;D$+ .S?@R .U>@RC6a .[B#lC0l .cA!!A@RD4? .|>A] /:@!!A@RC6+C$SE$q /G@@R /L@@R /QA!!A$SD6+E5}E.Y /WA@RA!!C$SD#2D6+E!~F+WF*K /XA;j /Y@!! /ZA1NAB?C/QD/:EC)E)xE*BE)wE;*FC[FBhF(RF&;F4%FB9G@dG2QGB7G.0G3CH3R /^A!! /uACwA4RBAc /{E5FF0e 0)?;H 0-B@R 01E7*EC'E,^E&IF5FF0QF5cF7BF=LF4|F/`F,=F,> 0QA1N 0S@@RB47B5TB*<B)wB3^ 0Z@*I 0fB*JC/WCB?C@(D!uDB6D&@D2MD)xE&?E/:E@3E5tE2'EC)F3@FC[F(RF;?F.cF0DFC8G@YG3oG5}G/XG<JGCEG,hG(TGBhG/hG9sG&EGCDG2HGB7H-aHC^H5[H#dH4mHBDH%NH/TH/,HAeI,oI-WI<KI8f 0g>3@C9h 0hA$DC.NC?9C5}D.F 0iA67B.UC>}C=RD!ME.JE3c 0j@$SA.cA5}B+qD!tD!pD;j 0k?(i 0o?CwA0fB/ZECz 1!@?rB!!D01D@.D5]D%IF3oF-tF1dF6tG+SG-kG$QHA- 16>6O 1?>1! 1D??r 1NB!!D67DAvE!~F.UF>8G@cG!tG9U 1PA/Z 1SA1NBB?EC)EC[F;iF*BF3dFBDG@dH9] 1T?$D 1UA!!B67D@LD$SD@cDAv 2'CB6EB7 2=>6O 2MABmB0SB?pCBsDC%DBzFBv 2QA0S 2U=6O 2c@6(B@LBClBBaC5> 2dA-N 3*??m 3-?4RB@Z 3.A.N 3;A1N 3@@@RB!!C?pC@. 3K>@R 3M>@R 3P?1! 3Q?1! 3R?1! 3S@1! 3^@@LB#` 3a@#lB3@ 3b@#l 3c?-NA#lA-^ 3d?3@ 3kA01 3l>6O 3m=6O 3oAC; 4%@!!CA] 4,A!!B1SB>} 41CBz 47B7bC@M 4BC1NCB?D#J 4O@0fA$D 4RB@R 4s>6O 4u?$D 5B@?mC@L 5DA6OB$J 5RA=1 5TC#`C5; 5[@$DB/W 5]C,^D5FE%rE0QE<rE3;E-nE7BF&IF7*F-pFC'F=LF:nF4|FAIG,cG0=G.m 5k?=b 5t?@RB!! 5v?@R 5}C$SC;j 5~BCvC&I 6%ABaBClB5> 6+A6cC0lC4LD3`E'7 6.>6O 67D.UE>} 6:@@RB&+ 6B?6O 6O@?rD01D5]F/{FAcF?uF6~F5;G7bG'h 6P@?r 6^B41 6`??m 6a??rC01C5]DC~E@LG5: 6cA6OBBz 6gA6c 6k>?r 6rA67 6t?@R 6zC)? 6}=@R 7$?6O 7'@?rB?y 77=6O 7G>6O 7bB#JCBz 7qA6B 7w>A] 7}=6O 81>@R 87B?d 8>B*JC?Z 8A=6O 8Y>6S 8qA.[A>} 8x>5! 99>6O 9HB6a 9n@-N 9sCB6 :%>@R :G>-N :T=6O :X@6>B$$ ;*A?pA/Z ;2A@& ;9@*P ;@A?pB#6 ;B@/Z ;dACw ;g>@R ;i?@R <5B1NBB?C/QD/:E*BE)xFBhF.0 <JA$DB/WC.N <M?/W <O@4R <t@*P =6B5TD47D,V =CC7bC5;C@L =GB+? =HA@RD+? =P?#` =S=6O =a@-kB+S >!>#l >-A/| >X@-k >c>!! >rAAl >|=@R >}A@Z ?9@!!B&L ?>?@R@!' ?@?!'@@R ?C>?m ?Z@4R@@ZACwCAcC0- ?b@CmA5$ ?n=Cw ?o>-N ?pB/ZE<5E4B ?qA!!A67BBmCC% ?rF;2FCSF-3F*LGBNG2cG6gG:nGA3G$oG5DG0QG9$G7MG@tG8IG&IH6zH%?H4`H5~H41H?7H%TH5;H6%H&'H>,HB~H+JH6!H'FHC.H>IH>sH1oH*CH6^H?OHAUH'3H!1H.CI:aI5CI0LI*>IB]I'|I(YI7DI:bI4LI9NI.'IBKI7qI2FI9ZI-0I3/I8-I.%I<|I>SI6SIB1I$6I.,I
*}I->I7uI&[I<wI;TI35J$EJ4sJ!aJ.fJ5AJ8.J+{J(,J2YJ6#J+| ?tC7* ?y@1NA#JBB?CBi ?z@!!@6+A6:B=H ?|B)@ ?}B#JBBiD/W @(A@ZB?pC6OC1UC!'CBPD0iDCz @)?!' @-@5$ @.A1NE%?E5CF!PFClF1PF9$F;wF:nG+m @0@Bz @3ACwA@ZDCx @9ACmB0PB)@B@MC5?CBc @<??r @LB@RC-ND0j @RC$DC*<D.ND.<E;dE/uF4,F?ZF;@F?>F?9F'oF+'FCNF&/F%IG2|G-(G>-G.FG3PG=aG#cG;HG87G4BG4^G2xH2*H9lH/gH>WH$QH>?H7ZH<}H*aHCcI/FIAdIB#I-.I&rI?2I$NI&]I3gI=jI*dJ=A @Y?4RACwA@ZB4BC0- @ZA1NCB?D/QD*BD)xE1PFC)F;*F@YF/:F#dFB9G.cGC[G(TG;iG2QGB7G5}G&@G;BG@dG3bGBDG3dG9HGBhHCDHA)H.0H4uH3CH/RH5vI;9IC^I@*ICF @^B5C @cA5TC2d @d@!!B6P @e>6O @s?!1 A)>@R A4?@R A5=@R A8A6P A@BCmC0P AK??r ALABm AU=>+ A]B@RBC;D#lE*z Ae>@R AvC.[C5TCBgE/KE&* B)@-NBAZ B+>-N B6>@RC4R B7>@R B9>@R B?B!!EAvE.UF%EG?% BHBA< BJ@A< BN@@R BPB/WC#JC&?CBiC<JD5tD/:D*JD5[E&@EC)E(RFBh BRA$D BSA.UA67 BT?.c@$S BZ?!! BgB#` Bh?@RB7$ BmC/ZC*<C1NC/GD#JD@ZD)wE@LE4BE*AE2=FCz Bn@?r@C~B.U Bq@0fA/ZC<5D)w BsA)wB1NC#J BzB1N C%A*JB#JB)wB*<C)xDC[ C)@$DD67D'oD5} C+=@R C8?0f C;B!!C@ZC4RC01C0-D5]D/{DAcD4BDC~ C?>A] CD@$D CE?0o CT>!' CV?!' C[@CwA$DB3@C/W ChAC; CmA!VA6^ CwC/WDB6D2MD#JD*JD@(E&?E<JE3@EBiF&@F5[F5tF+qFC)G?ZG9sG.UG)xG4OG;@G;*H4uH/6H<MHCD Cx?$q Cy@$D CzA67C.U C{@.cA$SB*K C|A7bB41 C}??m C~D,cE/uE7*E5cF,^F7B"""
ENDS = "$eL%TL%hF&BT&CV&FT(AU(OQ)=G){F**Q*iQ-]M.JL.WS.]K/pS0#T3nN4[M4jL4kL4{R5-J6+M8vL9:Q9mM:OU;DW?NKBUGCDWD3LD~RERUExSFbMH1KH2UIMWJ:WK]SKwUM]MNxJONFOSHP1GQ<WQISRrTS4FS8GV:WW+KWqSY!TZ.S[-M^!M^JE^RQa8UbHIbTEc#Gd$Dd3Md7Ld9Kd;LdRU"
RULES = "Abda Aciu Acut$ Adui Ajit Aluc Alui Arbat Areat Areti Arile Arui Arut Asari Aspa Atate Ateas Atest Atile Atise Atit$ Atite Atore Atos Atran Atrat Aunat Auta Azb Azne Azut Imbra Imbun Inca Incep Incet Inch Indre Inflo Ingri Ingus Inlo Inm Inno Inot Inr Insel Insot Intep Intre Intun Invat Qmpla Qnd$ Qndu$ Qnge Sedin Seza Snu Somaj Step Sti$ Stien Stiin Tia$ Tial Tie$ Tiil Tinut Tioa Tion Tios Tisa Tiuni ^Imb ^Indr ^Ingh ^Ingu ^Inl ^Insa ^Inta ^Intin ^Stii ^aSez ^alAt ^amQna ^bunA ^cAla ^cQnta ^forT ^gAi ^gAti ^intQm ^mAre ^rAce ^rAst ^sAru ^strAl ^tAie ^vAz ^vQn aSi$ aStere aTi$ aTia aTie aTii aTile aTilo aTise aTiu abilA adQn alAtur amAg anAto arAsi areTi areaT asAri aspQ ataTi ateSt atiSe atrQn aunAt avieT azA$ bAtr bTin batrQ bdA beSte biTi bilA$ brAr braT cAlat cAldu cAlz cAm$ cArcat cAtori cQndu cQntar cQstig cTia cTie cTii cTio cTiu caStig calAt calT citAri crAri creSt cuTi$ cuTit cultAt dAuna dQnc daTi daunA deTi depaS drAz dusA eInc eSi$ eSin eSte$ eTi$ eTii eTui eascA eazA ecAto ecaTi enTei enTie enTio eneS epAs epaSi eranT eratA erinT ernA$ etaTi fAcut fAtui frQng funcT gAtit gQndi gicA$ grAdi hrA iSar iSn iSoar iStii iTi$ iTia iTiei iTii iTio iaSi iaTi iascA iazA ibilA icatA ieSte ieSti igenT iinT imT inTei inaTi indrA insA$ ioSi$ iraTi itAm$ itQnd itaTi ituTi ivorT lAnu lAtit lTum latA$ lecTi liniS litAti ltaTi lumQ mArf mAsu mQnca mQnes mTi mbiT mbunA menTi mparTi mulTu nAtat nSel nStie nTei$ nTep nTi$ nTia nTii naTio natA$ ndepA ndrAg neSte nesA nfrQn nitA$ noaSt nrA ntQmp ntalA ntenT ntreT nvAt nzAto oTii oTio oaSte oasA obiS ogaTi onaTi onalA onatA onunT orbAr oritAti pTi$ pTii patA$ peSt pregA rAbd rAcie rAdin rAril rAsf rAsp rAut rQndu rQnet rTi$ rTia raTio radiT raneSt raneT ratA$ rbAto reSte reuS rinTe rtaTi ruSi sAnat sAra sArit sanAt sarbAt satA scA$ scAto scuTi seSt semAn serA$ sivA slAbi soT spQnd spreT stAp stapQ steSt stiTi sticA$ strAnu straTi susTi tApan tAres tAtes tAtil tAtit tQrn taTes taTil taTit tapQn tatA tenTi tiSa tilA$ trAlu treTi uSi$ uTia uTio uTite ufA uieSt uinT ulaTi umQna umpA unAta unAto unatAti unoSt upTi urAto usA$ utaTi vAtat vAzu vQnat vQntu vieTu vorbA zQnd zaTi zamA zatA zeSte zgQ zvA"
TOP = ['de sA nu In Si cA', 'the you to it is of']

P = {"lm": 1.25, "dele": 5.95, "ins": 9.258, "trans": 5.75, "maxtap": 13.973, "acc": 1.0,
 "strip": 8.0, "auto": 2.0, "valid": 4.9, "native": 2.678, "accent": 1.5,
 "accent_valid": 2.1, "unk_valid": 15.0, "unk": 18.7, "user": 10.0, "space": 1.25,
 "spacetap": 2.5, "beam": 32, "backoff": 0.92, "ends": 1.048, "prior": 0.94,
 "accent_ctx": 4.5, "split_nv": 1.275, "gapnotap": 2.5, "three": 2.0, "oov_pr": 0.6, "amb": 3.0}
ROWS = ["qwertyuiop", "asdfghjkl", "zxcvbnm"]
RY = 1.35
KW = 0.86
KH = 0.78 * RY
SX = 0.29
SY = 0.351
TO = {"ă": "A", "â": "Q", "î": "I", "ș": "S", "ț": "T", "ş": "S", "ţ": "T"}
FROM = {"A": "ă", "Q": "â", "I": "î", "S": "ș", "T": "ț"}
BASE = {"A": "a", "Q": "a", "I": "i", "S": "s", "T": "t"}
SIB = {"a": "AQ", "i": "I", "s": "S", "t": "T"}
ONE = {"a": 1, "o": 1, "e": 1, "i": 1, "I": 1, "S": 1}
SHAPES = [[t - r, r] for t in range(8, -1, -1) for r in range(4, -1, -1) if 0 <= t - r <= 4]
LETTERS = "abcdefghijklmnopqrstuvwxyzAQIST"
CEN = {}
for _r in range(3):
 for _i in range(len(ROWS[_r])):
  CEN[ROWS[_r][_i]] = [_i + [0.0, 0.5, 1.5][_r], _r * RY]
G = {}

def _num(s):
 return (ord(s) - 61) / 2.0

def _first(s):
 return s[0]

def _second(s):
 return s[1]

COMBO = "BCDEFGHJKLMNOPRUVWXYZ!#$%&()*+,-./:;<=>?@[]^_`{|}~"
IX = "!#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^`abcdefghijklmnopqrstuvwxyz{|}~"

def _unpack(blob, costs, pre):
 words = []
 prev = ""
 for e in re.findall(r"(?:[0-9].|[^a-zAQIST'0-9])[a-zAQIST']+", blob.replace("\n", "")):
  if e[0] in "0123456789":
   k = ord(e[0]) - 48
   c = ord(e[1]) - 61
   e = e[1:]
  else:
   i = COMBO.index(e[0])
   k = i % 10
   c = 18 + i // 10
  w = prev[:k] + e[1:]
  costs[w] = c / 2.0
  words.append(w)
  for i in range(k + 1, len(w) + 1):
   pre[w[:i]] = 1
  prev = w
 return words

def _setup():
 if "ro" in G:
  return
 pre = {}
 G["cro"] = {}
 G["cen"] = {}
 G["ro"] = _unpack(DATA_RO, G["cro"], pre)
 G["en"] = _unpack(DATA_EN, G["cen"], pre)
 G["pre"] = pre
 ix = {}
 for i in range(len(IX)):
  ix[IX[i]] = i
 pairs = {}
 for block in [[PAIRS, G["ro"]], [PAIRS_EN, G["en"]]]:
  ws = block[1]
  for line in block[0].replace("\n", "").split(" "):
   if len(line) > 4:
    a = ws[ix[line[0]] * 91 + ix[line[1]]]
    fol = [[_num(line[j]), ws[ix[line[j + 1]] * 91 + ix[line[j + 2]]]] for j in range(2, len(line), 3)]
    if a in pairs:
     fol = pairs[a] + fol
     fol.sort(key=_first)
    pairs[a] = fol
 G["pairs"] = pairs
 G["pc"] = {a + " " + x[1]: x[0] for a in pairs for x in pairs[a]}
 ro = G["ro"]
 G["ends"] = {ro[ix[ENDS[j]] * 91 + ix[ENDS[j + 1]]]: (ord(ENDS[j + 2]) - 79) / 2.0 for j in range(0, len(ENDS) - 2, 3)}
 G["user"] = {}
 dr = {}
 for r in RULES.split(" "):
  for k in range(len(r)):
   lab = r[k]
   if lab in "AQIST0123":
    base = BASE.get(lab) or "aist"[ord(lab) - 48]
    dr[r[:k] + base.upper() + r[k + 1:]] = lab if lab in BASE else base
    break
 G["dr"] = dr

_setup()

def _sync(state):
 words = state.get("words")
 if isinstance(words, dict) and G.get("src") is not words:
  G["src"] = words
  G["user"] = {}
  for w in words:
   _add_user(_enc(w))

def _add_user(e):
 if isinstance(e, str) and e and e not in G["user"]:
  G["user"][e] = 1
  for i in range(1, len(e) + 1):
   G["pre"][e[:i]] = 1

def _enc(s):
 out = ""
 for ch in s:
  out += TO.get(ch, ch)
 return out

def _out(e):
 if e != e.lower():
  for code in FROM:
   e = e.replace(code, FROM[code])
 return e

def _fold(e):
 out = ""
 for ch in e:
  out += BASE.get(ch, ch)
 return out

def _marks(e):
 return len([ch for ch in e if ch in BASE])

def initial():
 return {"on": True, "strict": False, "suggest": True, "restore": True, "learn": True,
   "words": {}, "seen": {}, "pp": {}, "keep": {}, "touch": {}, "pr": 0.5,
   "last": "", "taps": [], "pend": []}

def settings(state):
 return vstack([
  toggle("Bilingual autocorrect (Romanian + English)", state.get("on", True), action="on"),
  toggle("Add Romanian diacritics from context", state.get("restore", True), action="restore"),
  toggle("Strict: never change a word", state.get("strict", False), action="strict"),
  toggle("Completions and next-word suggestions", state.get("suggest", True), action="suggest"),
  toggle("Learn my words, names and typing", state.get("learn", True), action="learn"),
  button("Forget what it learned", action="clear"),
  text("Learning stays on this phone. Delete right after a correction restores your word."),
 ])

def on_action(action, value, state):
 if action in ["on", "strict", "suggest", "restore", "learn"]:
  state[action] = value is True
 elif action == "clear":
  for k in ["words", "seen", "pp", "keep", "touch"]:
   state[k] = {}
  state["last"] = ""
  G["src"] = None
  G["user"] = {}
 return state

def _protected(word):
 if len(word) > 40:
  return True
 for ch in word:
  if ch.isdigit() or ch in "@/:_\\#&=?%+-.’":
   return True
 return len(word) >= 2 and word == word.upper() and word != word.lower()

def _dict(state, key):
 v = state.get(key)
 if not isinstance(v, dict):
  v = {}
  state[key] = v
 return v

def _uni(e, pr):
 a = G["cro"].get(e)
 b = G["cen"].get(e)
 if a is None and b is None:
  return None
 p = (pr * math.exp(-a) if a is not None else 0) + ((1 - pr) * math.exp(-b) if b is not None else 0)
 return -math.log(p) if p > 0 else 40.0

def _lm(e, prev, state, pr):
 c = _uni(e, pr)
 if c is None:
  if e not in G["user"]:
   return None
  c = P["user"]
 best = P["backoff"] + c
 if prev:
  bias = G["ends"].get(prev)
  if bias is not None and len(e) > 2 and e[-1] in "aA" and e[:-1] + ("a" if e[-1] == "A" else "A") in G["cro"]:
   best += -P["ends"] * bias if e[-1] == "A" else P["ends"] * bias
  pc = G["pc"].get(prev + " " + e)
  if pc is not None:
   best = min(best, pc)
  n = state.get("pp", {}).get(prev + " " + e)
  if isinstance(n, int) and n > 0:
   best = min(best, max(0.7, 3.5 - math.log(1 + n)))
 return best

def _evidence(prev, w, state):
 if not prev:
  return False
 if prev + " " + w in G["pc"]:
  return True
 n = state.get("pp", {}).get(prev + " " + w) if isinstance(state.get("pp"), dict) else None
 if isinstance(n, int) and n >= 2:
  return True
 bias = G["ends"].get(prev)
 return bias is not None and len(w) > 2 and w[-1] in "aA" and abs(bias) >= 1.0 and (bias > 0) == (w[-1] == "A")

def _pr(state):
 pr = state.get("pr", 0.5)
 return pr if isinstance(pr, (int, float)) and 0 <= pr <= 1 else 0.5

def _prev(state):
 prev = state.get("last", "")
 return prev if isinstance(prev, str) else ""

def _ctx_prev(word, state):
 c = context()
 before = c.get("before") if isinstance(c, dict) else None
 if not isinstance(before, str):
  return _prev(state)
 if word and before.endswith(word):
  before = before[:len(before) - len(word)]
 before = before.rstrip(" ")
 if before == "" or before[-1] in ".!?\n":
  return ""
 low = before.split(" ")[-1].split("\n")[-1].strip(",;:\"”»)(«„“").lower()
 return _enc(low) if low.replace("'", "").isalpha() else ""

def _taps(state, e):
 taps = state.get("taps", [])
 n = len(e)
 if not isinstance(taps, list) or len(taps) < n:
  return None
 taps = taps[len(taps) - n:]
 for i in range(n):
  t = taps[i]
  if not isinstance(t, list) or len(t) != 3 or t[0] != BASE.get(e[i], e[i]):
   return None
 return taps

def _shift(state):
 out = {}
 touch = state.get("touch", {})
 for ch in CEN:
  t = touch.get(ch) if isinstance(touch, dict) else None
  if isinstance(t, list) and len(t) == 3 and t[0] >= 30:
   w = t[0] / (t[0] + 30.0)
   out[ch] = [max(-0.25, min(0.25, t[1] * w)) * KW, max(-0.25, min(0.25, t[2] * w)) * KH]
  else:
   out[ch] = [0.0, 0.0]
 return out

def _choices(e, taps, state):
 rows = []
 full = []
 sh = _shift(state)
 mt = P["maxtap"]
 for i in range(len(e)):
  typed = e[i]
  key = BASE.get(typed, typed)
  c0 = CEN.get(key)
  if c0 is None:
   return None
  if taps is not None:
   x = c0[0] + taps[i][1] * KW
   y = c0[1] + taps[i][2] * KH
  else:
   x = c0[0] + sh[key][0]
   y = c0[1] + sh[key][1]
  costs = {}
  best = 1e9
  for ch in CEN:
   c = CEN[ch]
   dx = (x - c[0] - sh[ch][0]) / SX
   dy = (y - c[1] - sh[ch][1]) / SY
   v = 0.5 * (dx * dx + dy * dy)
   costs[ch] = v
   best = min(best, v)
  for ch in CEN:
   costs[ch] = min(mt, costs[ch] - best)
  if typed != key:
   for ch in CEN:
    costs[ch] = min(mt, costs[ch] + P["strip"])
   for sib in SIB[key]:
    costs[sib] = 2.0
   costs[typed] = 0.0
  else:
   for b in SIB:
    for sib in SIB[b]:
     costs[sib] = min(mt, costs[b] + P["acc"])
  row = [[costs[ch], ch] for ch in costs if costs[ch] < mt]
  row.sort(key=_first)
  rows.append(row)
  full.append(costs)
 return [rows, full]

def _search(rows, n, edits, prefix):
 pre = G["pre"]
 beam = P["beam"]
 layers = [[[0.0, "", 0, 0]], [], []]
 found = {}
 ends = []
 maxd = n + edits + 1
 d = 0
 while d <= maxd:
  layer = layers[d]
  if len(layer) > beam:
   layer.sort(key=_first)
   layer = layer[:beam]
  layers.append([])
  nx = layers[d + 1]
  nx2 = layers[d + 2]
  k = 0
  while k < len(layer):
   s = layer[k]
   k += 1
   c = s[0]
   p = s[1]
   t = s[2]
   e = s[3]
   if t == n and d > 0:
    if c < found.get(p, 1e9):
     found[p] = c
    if prefix:
     ends.append([c, p])
   if d >= maxd:
    continue
   if t < n:
    for item in rows[t]:
     q = p + item[1]
     if q in pre:
      nx.append([c + item[0], q, t + 1, e])
   if d > 0 and p + "'" in pre:
    nx.append([c, p + "'", t, e])
   if e < edits:
    e1 = e + 1
    for ch in LETTERS:
     q = p + ch
     if q in pre:
      nx.append([c + P["dele"], q, t, e1])
    if t < n and d > 0:
     layer.append([c + P["ins"], p, t + 1, e1])
    if t + 1 < n:
     for a in rows[t + 1][:3]:
      q = p + a[1]
      if q not in pre:
       continue
      for b in rows[t][:3]:
       if b[1] != a[1] and q + b[1] in pre:
        nx2.append([c + a[0] + b[0] + P["trans"], q + b[1], t + 2, e1])
  d += 1
 return [found, ends]

def _case(word, cand):
 if word[:1].isupper() and word[1:] == word[1:].lower():
  return cand[:1].upper() + cand[1:]
 return cand

def _known(e):
 return e in G["cro"] or e in G["cen"] or e in G["user"]

def _align(full, typed, cand):
 n = len(typed)
 m = len(cand)
 prev2 = None
 prev = [j * P["dele"] for j in range(m + 1)]
 for i in range(1, n + 1):
  cur = [i * P["ins"]] + [1e9] * m
  costs = full[i - 1]
  for j in range(1, m + 1):
   v = min(prev[j - 1] + costs.get(cand[j - 1], P["maxtap"]), prev[j] + P["ins"], cur[j - 1] + P["dele"])
   if i > 1 and j > 1 and typed[i - 1] == cand[j - 2] and typed[i - 2] == cand[j - 1]:
    v = min(v, prev2[j - 2] + P["trans"])
   cur[j] = v
  prev2 = prev
  prev = cur
 return prev[m]

def _decide(e, fix, state):
 n = len(e)
 pr = _pr(state)
 prev = _prev(state)
 taps = _taps(state, e)
 ch = _choices(e, taps, state)
 if ch is None:
  return None
 full = ch[1]
 lit_sp = 0.0
 for i in range(n):
  lit_sp += full[i].get(e[i], P["maxtap"])
 fe = _enc(fix.lower()) if isinstance(fix, str) else None
 native_valid = fe is None or fe == e
 lit_lm = _lm(e, prev, state, pr)
 lit_valid = lit_lm is not None
 if lit_lm is None:
  lit_lm = P["unk_valid"] if native_valid else P["unk"]
 lit = lit_sp + P["lm"] * lit_lm
 found = _search(ch[0], n, 1, False)[0]
 best = None
 bestc = 1e9
 for w in found:
  if w != e:
   lm = _lm(w, prev, state, pr)
   if lm is not None and found[w] + P["lm"] * lm < bestc:
    best = w
    bestc = found[w] + P["lm"] * lm
 if fe is not None and fe != e and fe.replace("'", "").isalpha() and abs(len(fe) - n) <= 2:
  lm = _lm(fe, prev, state, pr)
  c = _align(full, e, fe) + P["lm"] * (lm if lm is not None else P["unk_valid"])
  if c < bestc:
   best = fe
   bestc = c
 if not lit_valid and 4 <= n <= 24:
  for item in _splits(e, ch[0], full, taps, prev, state, pr, fe):
   if item[0] < bestc:
    bestc = item[0]
    best = item[1]
 plain = not lit_valid and best is not None and _marks(best) > 0 and _fold(best) == _fold(e)
 keep = [None, lit, bestc, lit_valid, native_valid, plain]
 if best is None or (_marks(best) < _marks(e) and _fold(best) == _fold(e)):
  return keep
 if _fold(best) == _fold(e):
  if state.get("restore", True) is not True:
   return keep
  margin = P["accent"]
  if lit_valid:
   margin = P["accent_valid"]
   same = e in G["user"] or (e in G["cro"] and pr >= 0.35) or (e in G["cen"] and pr <= 0.65)
   if same and not _evidence(prev, best, state):
    margin = P["accent_ctx"]
   dm = state.get("dm", 0.5)
   noun = len(prev) > 2 and prev[-1] in "aA" and prev[:-1] + "a" in G["cro"] and prev[:-1] + "A" in G["cro"]
   if ((isinstance(dm, (int, float)) and dm < 0.5) or e == "sa") and pr >= 0.5 and not noun and e not in G["cen"] and not _evidence(prev, e, state):
    margin = min(margin, P["amb"] - P["acc"] * (_marks(best) - _marks(e)))
 elif " " in best:
  margin = P["split_nv"] if fe is None else P["auto"]
 elif lit_valid:
  margin = P["valid"]
 elif native_valid:
  margin = P["native"]
 else:
  margin = P["auto"]
 if lit - bestc >= margin:
  keep[0] = best
 return keep

def _seg(rows, e, lo, hi, prev, state, pr, cache):
 key = str(lo) + "," + str(hi)
 if key in cache:
  return cache[key]
 out = []
 if hi - lo == 1:
  if e[lo] in ONE:
   out.append([0.0, e[lo]])
 else:
  found = _search([r[:6] for r in rows[lo:hi]], hi - lo, 0, False)[0]
  for w in found:
   if _known(w):
    out.append([found[w], w])
  out.sort(key=_first)
  out = out[:3]
 cache[key] = out
 return out

def _splits(e, rows, full, taps, prev, state, pr, fe):
 n = len(e)
 lm = P["lm"]
 out = []
 cache = {}
 for k in range(1, n):
  for gap in [0, 1]:
   if gap == 1:
    if k >= n - 1 or e[k] not in "zxcvbnm":
     continue
    g = P["spacetap"] + (0.0 if taps is not None and taps[k][2] >= 0.15 else P["gapnotap"])
   else:
    g = P["space"]
   lefts = _seg(rows, e, 0, k, prev, state, pr, cache)
   if not lefts:
    continue
   rights = _seg(rows, e, k + gap, n, prev, state, pr, cache)
   for l in lefts:
    la = _lm(l[1], prev, state, pr)
    if la is None:
     continue
    for r in rights:
     lb = _lm(r[1], l[1], state, pr)
     if lb is not None:
      out.append([l[0] + r[0] + lm * (la + lb) + g, l[1] + " " + r[1]])
 if 7 <= n <= 18:
  for k1 in range(2, n - 3):
   a = e[:k1]
   if not _known(a):
    continue
   la = _lm(a, prev, state, pr)
   for k2 in range(k1 + 2, n - 1):
    b = e[k1:k2]
    c = e[k2:]
    if _known(b) and _known(c):
     lb = _lm(b, a, state, pr)
     lc = _lm(c, b, state, pr)
     if la is not None and lb is not None and lc is not None:
      out.append([lm * (la + lb + lc) + 2 * P["space"] + P["three"], a + " " + b + " " + c])
 if fe is not None and " " in fe:
  parts = fe.split(" ")
  if 2 <= len(parts) <= 3 and all([x.replace("'", "").isalpha() for x in parts]):
   sp = _align(full, e, "".join(parts))
   c = sp + P["space"] * (len(parts) - 1)
   prevw = prev
   for x in parts:
    v = _lm(x, prevw, state, pr)
    c += lm * (v if v is not None else P["unk_valid"])
    prevw = x
   out.append([c, fe])
 return out

def _restore(e):
 p = "^" + e + "$"
 dr = G["dr"]
 out = ""
 for i in range(len(e)):
  lab = e[i]
  if lab in "aist" and (i < len(e) - 1 or lab != "a"):
   for s in SHAPES:
    if i + 1 - s[0] >= 0 and i + 2 + s[1] <= len(p):
     v = dr.get(p[i + 1 - s[0]:i + 1] + lab.upper() + p[i + 2:i + 2 + s[1]])
     if v is not None:
      lab = v
      break
  out += lab
 return out

def _oov(word, e, r, state):
 if r[3] or _marks(e) > 0 or len(e) < 3 or _pr(state) < P["oov_pr"] or not G["dr"]:
  return None
 dm = state.get("dm", 0.5)
 if not isinstance(dm, (int, float)) or dm >= 0.5 or state.get("restore", True) is not True:
  return None
 if (word[:1].isupper() and _prev(state)) or re.search("[wykq]|th|tion", e):
  return None
 w = _restore(e)
 return w if w != e else None

def correct(word, fix, state):
 if not isinstance(state, dict) or state.get("on", True) is not True:
  return None
 if state.get("strict", False) is True:
  return False
 if not isinstance(word, str) or word == "" or not word.replace("'", "").isalpha():
  return None
 if _protected(word):
  return False
 _sync(state)
 e = _enc(word.lower())
 keep = state.get("keep", {})
 if (isinstance(keep, dict) and e in keep) or e in G.get("skip", {}):
  return False
 if len(e) < 2 or _known(e):
  if len(e) < 2:
   return False if _known(e) else None
 r = _decide(e.replace("'", ""), fix, state)
 if r is None:
  return None
 dm = state.get("dm", 0.5)
 dm = dm if isinstance(dm, (int, float)) else 0.5
 if _marks(e) > 0:
  state["dm"] = 0.4 * dm + 0.6
 elif r[5]:
  state["dm"] = 0.6 * dm
 best = r[0]
 if best is None:
  clink = isinstance(fix, str) and fix != word
  if clink:
   if not r[3] and (" " in fix or (not r[4] and r[2] < r[1])):
    return None
   fe = _enc(fix.lower())
   if not r[3] and _marks(fe) > 0 and _fold(fe) == _fold(e):
    return None
  best = _oov(word, e, r, state) if "'" not in e else None
  if best is None:
   return False if clink else None
 out = _case(word, _out(best))
 if out == word:
  return False
 state["pend"] = [word, out]
 return out

def _complete(prefix, pr, prev, state, scored, base):
 for lang in ["ro", "en"]:
  words = G[lang]
  lo = 0
  hi = len(words)
  while lo < hi:
   mid = (lo + hi) // 2
   if words[mid] < prefix:
    lo = mid + 1
   else:
    hi = mid
  i = lo
  while i < len(words) and i < lo + 120 and words[i].startswith(prefix):
   w = words[i]
   i += 1
   if len(w) > len(prefix) or base > 0:
    lm = _lm(w, prev, state, pr)
    if lm is not None:
     c = base + P["lm"] * lm
     if c < scored.get(w, 1e9):
      scored[w] = c

def suggestions(word, state):
 if not isinstance(state, dict) or state.get("on", True) is not True or state.get("suggest", True) is not True:
  return []
 if not isinstance(word, str):
  return []
 _sync(state)
 pr = _pr(state)
 prev = _ctx_prev(word, state)
 if word == "":
  return _predict(prev, state, pr)
 if not word.replace("'", "").isalpha() or (len(word) > 1 and word == word.upper()):
  return []
 e = _enc(word.lower())
 ch = _choices(e, _taps(state, e), state)
 if ch is None:
  return []
 ends = _search(ch[0], len(e), 1 if len(e) >= 3 else 0, True)[1]
 ends.sort(key=_first)
 scored = {}
 for item in ends[:4]:
  _complete(item[1], pr, prev, state, scored, item[0])
 for w in G["user"]:
  if w.startswith(e) or _fold(w).startswith(_fold(e)):
   lm = _lm(w, prev, state, pr)
   if lm is not None and P["lm"] * lm < scored.get(w, 1e9):
    scored[w] = P["lm"] * lm
 out = []
 words = state.get("words", {})
 for w, c in sorted(scored.items(), key=_second):
  if w == e:
   continue
  shown = _out(w)
  if isinstance(words, dict) and isinstance(words.get(shown), str):
   shown = words[shown]
  else:
   shown = _case(word, shown)
  if shown not in out:
   out.append(shown)
  if len(out) >= 3:
   break
 return out

def _predict(prev, state, pr):
 scored = {}
 if prev:
  for item in G["pairs"].get(prev, [])[:8]:
   scored[item[1]] = item[0]
  pp = state.get("pp", {})
  if isinstance(pp, dict):
   for key in pp:
    if key.startswith(prev + " ") and isinstance(pp[key], int):
     w = key[len(prev) + 1:]
     scored[w] = min(scored.get(w, 1e9), max(0.7, 3.5 - math.log(1 + pp[key])))
 top = TOP[0 if pr >= 0.5 else 1].split(" ")
 for i in range(len(top)):
  if top[i] not in scored:
   scored[top[i]] = 20.0 + i
 return [_out(w) for w, c in sorted(scored.items(), key=_second)[:3]]

def on_touch(key, x, y, state):
 if not isinstance(state, dict) or state.get("on", True) is not True or not isinstance(key, str):
  return state
 low = key.lower()
 taps = state.get("taps")
 if not isinstance(taps, list):
  taps = []
  state["taps"] = taps
 if low in CEN:
  if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
   x = 0.0
   y = 0.0
  taps.append([low, max(-0.5, min(0.5, x)), max(-0.5, min(0.5, y))])
  if len(taps) > 48:
   state["taps"] = taps[len(taps) - 48:]
  state["pend"] = []
 elif low in ["space", "return", "enter", " ", "\n"] or (len(low) == 1 and not low.isalpha()):
  state["taps"] = []
  if low in [".", "!", "?", "return", "enter", "\n"]:
   state["last"] = ""
 return state

def on_backspace(state):
 if not isinstance(state, dict):
  return state
 pend = state.get("pend")
 if isinstance(pend, list) and len(pend) == 2 and isinstance(pend[0], str):
  typed = _enc(pend[0].lower())
  G.setdefault("skip", {})[typed] = 1
  if state.get("learn", True) is True:
   keep = _dict(state, "keep")
   keep[typed] = min(9, keep.get(typed, 0) + 1)
   if keep[typed] >= 2:
    _learn(pend[0], state)
   _trim(keep, 200)
  state["pend"] = []
  state["taps"] = []
  return state
 taps = state.get("taps")
 if isinstance(taps, list) and taps:
  taps.pop()
 return state

def _trim(d, size):
 if len(d) > size:
  for k in list(d.keys())[:len(d) - size]:
   d.pop(k)

def _learn(word, state):
 low = word.lower()
 if not low.replace("'", "").isalpha() or len(low) < 2 or len(low) > 40:
  return
 words = _dict(state, "words")
 words[low] = word if word[:1].isupper() and word[1:] == word[1:].lower() else low
 _trim(words, 400)
 _add_user(_enc(low))

def on_suggestion(word, state):
 if isinstance(state, dict):
  state["pend"] = []
  if isinstance(word, str) and word.lower().replace("'", "").isalpha():
   state["last"] = _enc(word.lower())
 return state

def on_word(word, state):
 if not isinstance(state, dict) or not isinstance(word, str) or state.get("on", True) is not True:
  return state
 _sync(state)
 low = word.lower()
 if not low.replace("'", "").replace(" ", "").isalpha():
  state["taps"] = []
  state["last"] = ""
  return state
 e = _enc(low)
 pend = state.get("pend")
 corrected = isinstance(pend, list) and len(pend) == 2 and pend[1] == word
 prev = _prev(state)
 learn = state.get("learn", True) is True
 if learn and prev and " " not in e:
  pp = _dict(state, "pp")
  pp[prev + " " + e] = min(50, pp.get(prev + " " + e, 0) + 1)
  _trim(pp, 400)
 a = G["cro"].get(e)
 b = G["cen"].get(e)
 if a is not None or b is not None:
  pr = _pr(state)
  x = pr * math.exp(-a) if a is not None else 0
  y = (1 - pr) * math.exp(-b) if b is not None else 0
  state["pr"] = (1 - P["prior"]) / 2 + P["prior"] * (x / (x + y))
 if learn and not corrected:
  taps = _taps(state, e)
  if taps is not None and _known(e):
   touch = _dict(state, "touch")
   for t in taps:
    s = touch.get(t[0])
    if not isinstance(s, list) or len(s) != 3:
     s = [0, 0.0, 0.0]
    n = min(400, s[0] + 1)
    touch[t[0]] = [n, s[1] + (t[1] - s[1]) / n, s[2] + (t[2] - s[2]) / n]
  if not _known(e) and len(e) >= 2 and " " not in e:
   seen = _dict(state, "seen")
   seen[e] = seen.get(e, 0) + 1
   if seen[e] >= (2 if word[:1].isupper() and prev else 3):
    _learn(word, state)
    seen.pop(e)
   _trim(seen, 200)
 state["last"] = e.split(" ")[-1]
 state["taps"] = []
 return state
