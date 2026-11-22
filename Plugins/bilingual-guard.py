# ---
# name: Bilingual Guard
# icon: text.badge.checkmark
# summary: Touch-aware Romanian + English autocorrect, diacritics, completions and next words
# version: 1.0
# author: Rares
# enabled: false
# ---

# Taps are scored against nearby keys (2D Gaussian, learned offsets); a beam search allows
# slips plus one missed/extra/swapped letter; word pairs and the recent language weigh it;
# a word is replaced only when the best reading beats it by a margin (large for real words).
# Clink's fix decides words this list lacks. Design adapted from Hex's TypingDecoder
# (github.com/anomalyco/hex, MIT, (c) 2026 Christopher Langton). DATA_*/PAIRS/ENDS adapt
# FrequencyWords (OpenSubtitles 2018, Hermit Dave, CC BY-SA 4.0) and Tatoeba (CC BY 2.0
# FR) counts; shared under CC BY-SA 4.0. No Google/Gboard data. Internally A=ă Q=â I=î S=ș T=ț.

import math
import re

DATA_RO = """BAStia!ia1MlaOea1Ksta0LISi1JTi1Ji1Jl!mbrAcat_ac2Ii.pArTit/iedicat:nge;s^otrivA8Na3LreunA%umut>a+tPuScat1En]AlTime>aEuntru]Sel&at;i.TeleagA6Mg7Ne>Ti>m*re?ea7Ni<pciune=t6Ms2Kainte)aPlt;A3Lpoi2JcA_lcatPQntat>A4Nt/a$eapA5NrcAFp;Qnd5MeHm&i5LutWul4NrcVAm(QndHa=Ti=m)re7Mt<eHi4Nt`aTi(tUeazA<zi/heiat:id{AHe|Ti;riat5Ns(A<eHoare~ea;zi$oace:lo_tro3Mredere+a#datA/eajuns:pArtatPoialA&esc$rAgostit;zneSti:eaptA`ptat.ecat.fricoSAtor.ger^heTat*A/rijora?TiYt?tA}eazA_opat`zitoare?r.mormQntare.nebunit.oTi/atePt:a]registrare~area?atDsA_Si%rcinatA/cris3LeamnA:mna$uSi%Ti:mi_rat2NtQi:lneSti=ascAWscViWmJre+a>i7Nt4MmplA7Na>re8LtWe:rziaKt|e>re=i/eleg<s/inde;s$oarcA7Me}TiXm}re4NrcVi5Ns4Ltdeauna3Lr4Me&abA<gAJa5Nb{AmJri?leVa|Ti)m7NreYa7NtVi&g(i=me(ul_u/unecatAVricDvAT;AmGa<Ti{rea6NtPaTA$eTeUi[siNtiZSah.mpanie2NnsA%a:e;leDpte.rpe2Nse1McoalAGa^li;i-edinTA{a#f$uFl;e;ui]rif1Ei.r[oc^at#fer;ul]setele-terge:sDi3NTi3Na:TiFi4Mm:u3Ke3Ji%nTA<a{ifice3Nm^re%i`le3Iu4NtMTAri:i_le1NarAEa1KiDe]gAri/arADiDn$A3Le:Ti_a%m^tA:aEut.pA^a_t/i0Ea1JS2Ha$dar#ezat2MteaptARpTi5NtHAmHaWTiWm=reJt(e1KTi-bTine.andonat]by2Nia]ordare]senTa`tEolut;vit^urd{ANcTiune<i=le2KasA.cepTi;t<A(aWt%sEident*ul~luiDeSti(a3Ma4JstA6La3Mea5NSiPi%a;Si3Ml4Na5NSiFe;a(Si`i:ui3Jst5La5Le6NaHi&orGui2Jolo^peri)S=re)t}A3Mrd;at.t/ele^iv`itate^or/ualA2Ium_a^zaTii&t-dApost/ugatOQnc#amPptareaOeseaPvAr6LatXA>a>e>ul6Mul2MicA$o]mir]n]optat$r_A%mit.resAUa#u3Nc%AFe;Ti;mRi/lt^nA:at3NsCer$oport$ulNfacere)aHi=le3LrA%a.ecteazA2NlA%m$a_TiFt$e$iPu#rica[gATatOent&ulCh1Gi2La2NbA2Hci.ureaCjuTiEngUA5MeVmUi4Ms3NtFA&m4Ma;TiGt4Ne4Mor6Nul1JlDAturi#TiFi.an/rmADbEA$astrAWu/e_rt/i.cool2Me/a:rgA^e/gRe&re=a{i=le:i/rg;a<t`i{c3Ms$x#geria.iceDo2Nt3MAPa3Nceva4Nineva3Ne%le:rnativAEfel/or;a/uiaFl1Fm2NQndoi(uA.abil/ndaObele^ii^ulanTA.eTit/ninTare>tPricaWn>A>i?i<ii/stec#iazA;aEce^nFte(SteKi6Nsc&i<Ti<ri<t]prenteleDuzant|A.y1Nn]a^lizA.chetA.d/yOgajat^ela`es$lia2Ji$iPmalVe)le^versarea.na^e/ie]terior^renament{or>ul2Nul:at%uiPme:it{A(e$nT`a{t1MpA/rare|a:eaFut2Na$r:A_TinWe_at<ul%e;nt_iTiaRtamentYtul.ei$l:e_ul2Loi.recia(ez$ilie_nde;s3Loape:pia=Ti)t}AVe=re{i&oRximativ]ucA:at1HrDATiEtFa;TiUt.anjat3MtA%e#de2IePstat.gint2NmA$aRtA;aPe%le]ogant#s#tA/a/hur/icol=ul:ficialA:st.uncUA{m`a<TiVt`e`iNsculTi&t6NA|mVa)Ti)t{e:nd<AVeUs&ziDearA^mAnAtoare4Menea#igur<A<a=re^stent>A2LtAzi3Ga3Lea`ptA3Nfel2Nupra-tQTia3JtFaReaOac:A%at_ul.enTi(aHeFt;A^rizat.ingUe;iRs^tudine~a.mosfera]rage:s2Kunci1Hu2Nd$A/e.gustDr/ulDstralia.toRbuzJul:rul2Nzi:Ti:m4Lt!vQnd]ans`at:taj2MeTi3Ka%i4NmRu3Km/nturA/re_tisment<zat=ezOionUul]ocaTiUt(ul2Kut1LziBbA.T.ga%t2NiatGul^eTel5NiViRte#nuiescOrbaTiWi5NtHul#taiePrQn{A{i(ulPutDut%urA{a<i!a.Ti]ftA.g^A/ajele/i.iaEe]l^con$tA.nEcA:a^dA:a3Li4Mi:lorOr/A$cA:a^ry.schet/eball.tAPe.zAEa^eazA-eTi2Na$tEu.beluS=ulOi#m#n/zinAOre/lin]tty[iblia`e&otecA#cicletAXa]g#let;e<le;ul$l%y2GneFInTeles%leDrou5NlOsericA!locat!oalA:aOb$by.gaTiRt&A]liiEnavVA#mbA_oane.rd2Mston{ul!rQnzA;a.aTe;le:ul^dPvoPzilia.ian]ownOusc-ucATi:tAriaXe;ar$atA3Nur&A&ie&os2Kn3JA3Me3NiRca;iiUul=ui.ton]ze:le/unar0EcA]Tea#ci.dea_rea.i
.lAtoresc=iXaXe>t/cat^durA<a.maSA;a]pSuni$itanWeWul2NrTiGle/ei$or`a$ui;a.sAtoreSti>ascA*scWi>Ti>a*eKt2Ntre#utAm_Qnd%a&Ti;m`re)aUtDzut!Ind-QStig(A|mHaJt(e<iDTiFvaDine5Nle:i&i#mp.nTi3Hd:vaPtRA;reT_QndRa`t%eUc(ul2Jt/A3MeRodatA4Lva1Ha]d/A^a:vru)l$eEou;ri/rul2NfeaUua_nea.iiOl/culator+rulEd:A3NeFa/ifornia%tate}aPm_a$ul2Mm3NerA5Ma&e{i<le/ion<ul^panie]nada`ian:pea$cer2NpPAt`ulPabil|A/cana/italA)a3Nul`ui]r/dul3Ge/ierA<a/l_osPne&a^ol3Mte5Ma;r%ier=ul:ofi|i2LsA3La$eRi:le_tA/tel<ulDuTiEtFA%e$zA4Ma`t2Nz3Nul:ri1Fe2La/ScAEi%ulElaltA/rA%tAPsFul2Kea2LiElalTi2JlPAlalt3Le:bru%lalteEor$ui_lA#ntruVl2Nr^c_ei`tareEe_Ti:m:re<aPi^tAm%atPul4Nt2Iva.zar!harlesUie`otteDeamA$fPia%eRle/ltuit/m:aUtEstia(eVi=le<une2Jiar/cago$na_ezA/peS_ul/ria/tarA]loe#ris.uck1Ni]aDnAPa3Mci`sprezece;zeci3Je:ma4Kva/ste&it#ocolatA>aOteSteViRascAFscPi:Ti_nd4Nt;ul/yOuda5Nt(A<e!lAdire)a<ii.aireEr:A:kEsA%a:icA.ienTi=i;t<ulEpA#ub:ul[oS/mar.adA_a^sta.boarA%rQt.d/ul#lT^egi<i{u`ul/onel|e|ul#mandA{ante?ul=t^is/oarAEpaniaJe*i|i4Nlet=A;icat_orTi<tA|ament+entul:uter$un#nStient{inTA?a$Tine$cediat&rt=ul:urs/damnat:iTie)i>le|onatRuc(AHeWre(iUs^exiune~a^firmat_lict%orm<tabil:uz^secinTe:ider*A*are?t;liul_tant`rui>ascA}esc*t~APt_a&ct=a|ez4NeazA4NinuA>mWa>TiXre*t=e)i_rA;act*ulUol=a)ul:ul/versaTia+ie_ine{g=e|iVsOpac;i<i;ul/ie4Mi5MiGlor4Ml;Arie5Nul)ui.rd3Nect(A:ea$pRul<uiOstA:a`t%um<ul]vorCrAciun=ul.avatAOeSte(re>a/a%dA:scAFt;urA3Id4MeGTi&a<i6MmUm_inTA=a;t/eazA/ier(ul:on^mA/scGut3Kzi4LutOimA%a:e&i%inal>i>ul$zA.ud1Fu]ScA#Tit&ulDiPva]lcRare;tPoare=a/turA<a2Hm/inteEpAr(A=mWturiHa7MtRereViEvaDnoStiWnTAFaSte*Ti>m4Msc6Nut>A.plu]rATA;at`enie3MQnd$aj&os;ulRt&A$ent/ge/iosPs_A%a%ul/te&a/vA#tiaRe_i/remurDvQntVulEinteWle>or0IdAOm1IaDTi2HcA2MiOn$iel$ny$s_eazA`z{i2Hr2Kt3LA3Na$e_le^or;eazA<z=iUiaVtA2Mu.vePid1De.SertEi/teaptA&pt]Tin;eDa/nPsupra2JcQt^embrie3Ki:de4NsRzia(e{i^laraTie=t.dicat.fect{e]geaba_t`e<le&ulPrabA2LjaEun]licioasA=s3Noc]misia^ocraTia^ult.ntistDoarece/camdatA$datAPparte/sebit#pASit:rtare/artamentul6MePinde^ozit^une:s#ranja=tHeazA)zDs^chiSi(d7Ne>TiHsWA|e<zi_operiYt:rie%urc=A=a*t=i^enat_ori:rt3Nigur$pArTit4Jre/tinul:ui5Ll{A<e#talii=le{u$ectiv}ulOveni6Nt$iiRnUAUe3Mreme#zamAgit:stru^gustAtor^vAlui:oltarea}t-iavolul#cTionar?ul/k.ferenTA*a`iTiVt)AWePicilWA=e`ultATi>ate2NmineaTA8Na2GnPTi;i^ainte$colo^teRr5Le.recTia=eGt<or*ul]scuTia)e`rs)ul;t(Am<a)tPearAEpArut:arA<i:onibil;ziTie|tiv%usPtanTA=a_rAm&acTieWtiv<t`ugA)eVs=A]vorT{atCl2Me]uiCnA]aCoamnA5Na5Me{iVlor3IrFe_mAUe]cEtorVeHul^umente~le2LiPlea^sprezece2Nlari.meniul/n%iSoarA?aUlor4Nul6LeVui#n^naDrPeSteViRa&mFsc3NiRTi%m:nTA(aFtPmFiUt<or]s^arele;ul2KuARzeciPa^gOvadA/edi(t%zi{le1NrOA3NguTVA{i2NacuUluiEgAFaFosteKa%ul(eOeaptAVa3Npt5MateGul<rile]ogatRuri2Num4Mul{ui`rileNuOS^man<i{ul]blA_u2LcPA3Me%Ti%m3Ni]lap`ulPce_iuri#minicA)a^neata6MvoastrA5Mzeu8Nle2JpA#r^APa%t`a$eazARreVa;i`os:ze2Ms!vDs0Fe1HSti#uat1Ia[chilibrulFpAGa`e(i]onomia-d#die]ucaTia=e!fect]icient.ort`ul{rile-gal_e.oist1Hi1Hl2Me/ctricA/v:i&i]ibera)t/minat^zabeth!mily.ma]oTie!nergiaVe_veazA2NglezAHa!pisodul1Ira/Ti3Ni3Lm3Mu.i
c.oare/u:l!speranto#t3Fe!taj%ul1Hu#roRpA!veniment~e]idenTAHt^tA1Mxact/men(ul#celent>A%pTia=e/ursieOemplu/rciTii2KistA;aVt;e<nTaOperienTA?a{ment;tPlicVa)Tie~i)t<i_odat`zie/resie.traordinarRem0MfA#cQndPea;i&m3IutUA&e2KrA[Qn1MaTA3Ma#bricA<a2Jc3KA3Ie4MTi%book4Lm3Ji^tura$ultate?a.imos#ls:A:e2Mmilia6NeWi<i|le.ntastic:omA<e2Mpt:e;leFul<ui2MtA3Na#voare|a_rit|A.zA!bi[eTei]brA:uarie.deral2KlPicitAri_eEul_riDmeiGa5MeGle<orOreastrA*aPiciTi(re>a6Mt7NA|e$mADteRle&or/iTA&a1HiDTi2Je3Kcare/r%binte:ul]gurA2Li$cA4Na:ei/nTA;eFdGcA2Nlm%e;leRulDmOnal;A;ul/e^landa]r^e$mA%a2Lu3MlRe%ui.x.zicA;e-lAcAri#oare<aPri&le.uent1Noame3IrteDcPul_ri.losUeSteXi(ascAVscGi<Ti(m<ndHt)A|e]nduri#rTA%a&t:elePmA:a;t^te2Gst:ulDtbal/o_grafia+e+i!raTi&iPnTa%cez7NAJaRk3Nte5Mle(ui^zA:e.ed2NicAPg:ider#ucte{le/moSi5MasAJe5Ms:useTeYa/nzele-u]g/AEi_mFt.m/a%t;ul/eazA:z.ncTie<ona?tKeazA$dRul.rAEat^ia_oasA&sPtunA(a<ii.seseZgAseSteHi%ascA4Nsc3Mi:TiFm4Lt`A]teSte:sc/i:t1NQnd%eSteJi`aHm{scA5NscRi&m;re5Mt:ul;ri=le#t$ul-alben<A#rA^dA/y2Mta#urA.y]z[eamul$nta]loasA:s.nPeral|e=ul/iuEul:nchiOorge.rmanVA<aVia=ei!heaTA]icesc:i^nion[loanTe/balA/nT^ria#umA%a_eUSti`le;sc-oalA:eOl$f[rAbeSti`sc_im$dinA(aPmadA#abA/ce$de$s:A/tis:uit$v_e_idA]eSeSte5NalA=aUli=le4Nit<APa_cA^g/le3Mu:tATi`ate.i3LjA4Ni.oazA&nic}A3Nzav(AOup:ul!unoi`ulOrAEaOst:ul.vernVul>ui,hA-Qrtia&e!abar2Li3LdeGTi/nA:aReUle.nk]os#rry$tA_a1Lei]lenOnry#y[itler!mm[o.T/ii/ul]bby.lOtArQtEel&ul]ward[ranA-uh0Ii1La#d^ul#nuarie2Kr^ASi/bA:a$nAFaOsAOtA2Mu1MdeeFa$i:le/ntificat<tate~eaOiot;ule1NeSi:Ti%m%re4Nt.ftin{A2Ni2Mri/ta;reOsPe[isus&e-legal-magina=t<e)a|z<i2Mediat^ns`A.pact^lic(at:or/ortanTA8MtLAYeFsibil/resia=onant+at[namicul.cendiu^ident/lusivPredibil.dia:cA`iuRferent.el:ul.fluenTa^ormaTia?eLi?ile=t.ginerOimA4Na:ii]spiraTie/tanTAPulA.teligenTaYt~tA:nTionat~eazA~ez:resJantYtAXtWeazA=ul&ior*ul`naTionalVet;viu&zis}A3NrA&mRa&Ti;re)a5Nt%e%iRu#util#ventat_rs^itaTiaVt[steTPoria(e.us_e-t#alia{nACubeSteVi_a4Msc$i:mRreVa;iiFt`AUaUoUul=e#lie.nie-zbucnitBjack_ie%son]f#keOmes^ieOne.ponez)AGia.son[ean.ff^uit.nant/ny.rry]sseNim$myCoacA%e2NcPiPul:ri<leOe/y2Nhn%ny_son.i.nes2Ls/hNucAm_rii=le%tor|ulPa_TiRt#decAtor?ul;a(tA.lia_e2NmAtate]piterDr^at^nal{ulEul@karen#te^ie-elly.n.vin[ilograme:metri.m!m-yleMlAsAm3NaRTi4Mt[QnA3MgA1FaDSi.borator#c^om/rimi$ul.dyDpte&le.rg/ry2Ns3NA$e#tinA]udA/raOyla1Je.Sinat]cTia;e`i#e2NgAturAWa^alRt`A;ePeRa^i:i:le$ume#mn.neS/t.o]u!i2NberUA`e`i&tate+a#ceu;l]der;ul]ft:ul]ly2NmbA4Ma4Ni`i&le{or/itA`e]ncoln/daEiSte|aVit*A%a%e#psA%aReSte`sc_iUt.re#saPtA%a.tere1Koc/al`A/otenent?te^uiTi`ascAGeSte*iHsc`m&t4Ll`uiRri<le]gicAOndra2Kr^d]s.uis]veSte/iFt&urA=a|i[uA3Nm2MaETi3Lt#crAmRa;Ti`reaGt4NeazA5Nz(eVi4Ku&l5Mri7Mle}or/y2Hi.ke2Mme4La^iRi%nAGa;ileDnA3Na/eaPgFA%i;me=aRul3Mi%i.p/Ti/tFA;mRa&t%e/ul0GmA2LcarDnQnc6NAVeHi/uSi#r^cuS^ii_t`atA/turie|sit/ulOsurA`a;i]tasePuSa1LQineRi5NleDnA3NaPcAmFa;Ti5NreJa5Nt/drA`iUu-a2MSinA5LaUi<i<le]c]dridDgazinWul^gie^ia_c_e2Fi/l^muTA^or]jorUitateaDmA3KaEeiPi.ndat#rTi$cat3JeRa%le/fA^ginea3Ni4Ma:eUi:na$k/o/te%ie;n%or<i3Jy2MsAPa_j^cA.tematicA?a_rial
/tOx^im`A!da-e2Ia3NrgA#ci%ul#dic;al=A=e(ment+te~tele`inA&ul:e%u;l{ui2Li]lanie3Le/odia<e#mbri<i&u/oria<e.nTionat^iul]rciPe:le4Lu3Lg4LeGTi&a{m5Lm4Mi/iTi:tGA`at3MsFiDsaj;e&ul/e.todA`a`ePri_oul2Iu]xic1IiOScA`ri%a`TiUre$to2Nc3NAPhaelEiEul2Me/rcuriRe$zulDi#jlocVulOke#lA$e/iardeFoane&n_tar=e]nA^TeaRi;leUt/cinos&unA=i3Ie/ge&a/istru$t4NeUa3NunatJA=e;eFt5Me.racol$easaPoase:s&ul#siune)a/s/ter]zerie-m[oS.alePrA%eRtAGe6Na#bil`A`ul2Md/A$alitate$el:rnAPul_ri]lly2Mment<an<eHul#ndial=A^edA/struDrPTiUi^ganPi3Nt]schee2NtivUe{leUul^ocicletA:r&ul-r-uScat2LlTiGme4Jumesc{iWmWt>A3It4NA4Ke:or.nTi3McARa%eSte=i;ascA&sc%it{or$te`le<ui.rdar<A<eEi:m4Mt.t/APat.zeu`lEicAGa0NnAscut-aS^teUre/ul#Tional}A2LibaFii]sol$ul]te^han^urA&a<l|A=e`ii.vAPa^e[chen1Ie]aTaPgrA/pArat2NbunUA&iVe.cazuriEesar=A=e&itA.fericit.gat`iv^re:iRu#norocit?A?ul?ule.obiSnuit]poTi_ata:liticos:tul#rAbdare$egulA^voasAUs.vasta$inovat3Joie;tDwNi2LSteOcAieri3Ji4Mo5KdatA4Nun<a(ul$kDmAnui3Keni3Jic#nge/s.sip#vel&ul[oDStri2Mapte6Ma3LstrA6Me2Ji/embrie^i.pTiUiOrd$i^mAFal<A3Noc;oSi<asA(s&ul%i2Lstru#ta2Ku3MAEaEl-r1DuOmAr5Nul3Mai3NeRSte<i4Lle:re<le`oasA%sc^i_mRt;A#ntA%a0Eo1Kameni6LiHlorOrAPe_care]se[bTii_nGe&ut#iSnuia>mWt>A3Ncei<ul=rile^ect{e.ligat.osiTi5NtVAOservat!cazia;e#ean`ului#helari*iEi4Mi_lor:ul#tombrieOup%A:a;Ti5NtVA_e:i1NdatA]ihnA`eSti!f.erRARi`mUt%tA&a]f#iTer{ul$cial-glindA1Kh1Mk#ay[liver1Lm.enirea#oarAUePrRIFQt2Nul4Me%ui[n]line#oare<a^ratA-oh-pTiune<i]era;Tia=e|une#inia.ortunitateDreSte(i%ascARscEi:Ti%mFtDt^sprezece/zeci-r2NA2Ma3MS:e4NulVui]b.dinGe(le;ul/onat2Me/le/z2Li/bil$cQnd;t%are4LeFine4Num^ginalPunde[travA-u#A/leMpA#Tit.cAlitEatUe/iiOdure{a`ile2Mi.lAria<e2NmQntVul*ui.puSA`a#r^AseascA<sc&iVt$Ti3NeaRreVa$inTi7Ni)lor&teEulRt.sAri(le/trAm&a{Ti(t&eazA<z|e=i[InANQineUa2KnA/a-a.Saportul^i2Nce%a/het<ul/ient=ul]ginA`a`iDhar&ul]latul^mA.nicA$taloni+i%ofi)i.pAOr$APcFA:a;re;t/don3Je/fumulPi:ezRs%u^k_er/ola3Lte5Ma;ner>ul`r_icipA>at;dOs3NA%re<a^tile/ul2Nt/rick4Mu`lea&zeci$ulOulPzA.zA1FeDSte;le;rA:i`i.deapsA|a]nsie3Gtru#reche%te3NfectWAPicol;uloasAKsRoadAPmis<iunea<ul;tHe=Ti3MsoanA)aJe*leUnal>A>e.scuit3Lte#teRr^reacA&cVe7NreLa{iHut-hil!iaTA:a$n/rdAPtrA2Mc/AturAEioareXle&rVul^nic^tat_urA.ele&a/ptPrdGe(m<re>a5LutRzi$sA_e/tre.lot.scinAPicAUa;i<le/tA:ol<ul#zza1NlAcea5Nre=a:intA4Nut(A^nuieSte{t/teSte)i&ascAUscRi;Ti`mGtOQng&A;QndUe{re;i%s2MacRA4Je:iEjAEn%etA(a_tat;e<leFul&ri)le$stic/tA_a2NeacA3Mc4NAm4NaUTi;m;re|a5Lt4Ne4Ni#ictisit?oare+or^mbAUareEnFA_eOoaia&e/iiEuA:aUt]uSEs[oStal2JTiDartA`a;e$tA4Ie.d$ea/ul.ezie;i.ftA_iTi5Nm#liTiSti+i6NaHe)iVst}ul%ticA=a=e=os]na]por;ul/ularOrTi`le$c^eclA/neSte%itPt:ocale;felul%ughezA+a^umbelul2Nsibil|A=itatea|ul$t:ul2It^enTial$riveSte|scHit>A.veSti|leFsteJa<itOzA$a$e:le$iTia<e-rAjiturA}iOQnzUul#actic=A$fOeSedinteLelePTRul&rile3Ja:jmAEcum/dauPfer<A<aWt*A<i/gAteSte=sc(iTi|mJt*A/miu{l^ot/sA:iuneRupun>e^tinde$zenTa|iVt=at%int|A.icep{i{ut3MetenWAJaWe7Ni>a8Ni>lor=os7Nul?ui/m_A;varA*a4La;r<ul:eSte)i;leUscFi;i`m5Mt4Mul3Kn:Si_T;esA=a;ul%cipal?A~a%d;AUe<m4Ns:trHe/vat<AFeSte|i;sc:i&Ti&nTa(dGre)a&t.oSti<i/a
spAt>AGtA(e/bA4Labil:e4MlemA7Ma7Me*le$ces<ul/duce&s<e{ul/fesionist<oarA+aJr>i~iKul_it:undPgram=are)ul`esePiect)ul^miTiUs<iune?eaGt/poziTiaYeYi?ileFria<etarul?tea(ile<uWl:unerea3Nst;esc`ia(e<i|le`ule^tecTia>e&ja{eazA=z>e^voacA`care|t]udent[t[uScArie/ti;ul=e2KTinUA&e&iOblic{e<ul2Ni^ul]lover2Nn$AEct;eUul3Me%Ti%m^gA2NrPta`Ti&t2Ms^A2MteTi4Ja;iGm;u4KmRreHa`ileGnicXA*e>i3Lut,rAbdare|a]cealA#iDmQiRnUA5Ne<Ti(m3Mas]neascA$i:TiFt`A.pit#spund=AJe6NsJul>ri~ile<zi]tAcit2Ju/l2NzboiVul*ui_unare!Qd$eDndRulDsOu/l.zi[aTional.chel#dio;ulDhat;ul.nADpid;A/ortVul#r/eori.ta%t#y]zA/na[eTeta/inutOaPl%A_eRitate~a&zatDceRnt_pTionat/iproc^omandat`pensA/unoSti(aSteVsc>AtorXut]d/ucere.fer;i/uz;AUatOgeRle;ui/inA&a_unea$ret3LulAUa;iVle|or#laTia(e<i$e/igia.marcabilA.nunT(aWt<e<i.par;a(t;e3Lede:t;A$rezintA^utaTiaOspect=A|at=ul_ins&rA%onsabil~ili?ilitateaPtaurant+tulFul.tras]uSeSti;sc%i5Nt]vAdEedere:ni(t/in:stA{a.zervA$istA^olv<AmVa)t<e:nabil/ultat>e?le*ul!ichard^k.dicUA`aVt|A`e&ol.ma.o.sc_A:ul;ri]tm-oSePieRiEu]agA/ta#bert^in^otOchiaUe/k2Jg^er.l/ul.mQnA;iaPaRn`e;tic;ul]ssPt]y.zCuSineOgAmPat.pePt]s$APia!yan0DsAOi.lbatice#nAtate*a;oasA(s2NptAmQnA8NaKi?i#rac`A`i/bAtori?m/i%t$ut&atDturat2KuNInt!QmbAtA#nEgeUle^ii1La.bia_e]c#lAPa_riu=l:tA3Me^ly3Nut`Ari`are$vA_areUt:ez<e<iDm3Mi]ndviS.rA$ah/cinA$e_a/i#t^ul2Ju!cApaGt/ri$zut.ap%A%e:iPun;ul#enA:aDhimbVA|m=ri~leHa)re?a7Nt(e(i{ul.oTi/atAUe<m/pRul/rulEs$t:t2Nrie%i&tor4Ms&A`eGoareYa<ri`ulFuOump&A;eUo;ulePrtUA`e$zAFaTi4Me1Ge]amAUnA4Ma/n3NrA4Ma]cTia$olulEret<A{arA(e(ulPundAVe%ritate~eaOmn:al<ul;t:e:ul]ninEs:ibil:ul$timent+e+ele.parat$tembrie#rgent/ie%oasA5Ms^viciileJu*l`t#teDx/ual<A:l$y#zonul-fAtuit.Qnt^rSi6NtJul#at%ul;ri.ert]inte]orAie1Kigur5NA5ManTA*a&i]mT:ea<m4Mi;Ti`m5Nt/onPplA`e5Nu3Lt:AFeDncer<APe3Lgur6MAHaVi6Nul/ucisOstemHul.teEuaTiaWe`t[lAbiciune;tOab%A_e_i/vAOujbAUa-mith!oT3MiaRe&i3Nul&uiOareUle(ui_tA;a]cial{A{e_etATii<ate?a.l/daTi=i&t^uTia(eOmn.rA3Na.sEit!pAl%at]aTialA&u<l$lA/nia;ola^rgeRt3Nte5NleDecial)A=e;i%tacol?ul/li3Mr:AUmRanTA)aFiat=A&e;i.irit<ul3Ntal<ul#ort2Mre^ijin|ul2Kui3Kn4NA:Qnd4JeGTiUa<i<m{uUm3Is%e[t2NAPm^pQne{ulPtea.Qnd_gAUaDaETiUa&e^bilA(it3Ki^n^rFe&a3Nt%ele<or:ul<ui3NuDea$le$veOiclA;e/l:ul/nge:s.omac{ul/p#rAin<A)tateHe<i:zi<i{le$QnsPadAUa^eet/icAUat;t:gA{t#udenTi>i(t|A:iaVt(zAGez=e=i`ile;u<l/pid-ua2Lb$iect)ul#cEces(ulOd.ferA;iVtEicient?A?e^lA%etVul.gerat;ez]mADn3NA_mPa_Ti4Nt$e_t&ulPi3Gt4LeTi5Km#pA_ra{TiHt)A/aPer&i;market$ort(a/rafaTA;veghere(ieTui?uit.rori<i{lePprinsVzA/sA_e2Ms/Tin(e/an/pect|atOtAPe,tAcere(a$ut2NiPat2Ju1NQnArUA.rfA3Lziu1JaOTi.bArA`a/lou{lDci.i$e2Lle:nt<at2Mre2MtA4LlGui3NaEoeba]xe$i_ul.ylor1Ge.amFA/tru.d]hnic:ologia.lefoane6Nn7NulFvizor+ulOm/a$eRle/peratura_lu_orar]ndinTa$is.oria;e#ren;ul/ibil$men{ulRinVA)mHa|Ti7Mt<e<i^ry#st_e%ul]xas/tChe#omas-icAlos|ule]m^bre/id3Jp4Kul(ui2Ine:reUi2Mp/ii3Nul`e-o2KTiFi#aletA/mna3KtA4Je2Mcmai]ki/yo2Gm$my#ny]pit#rt2Jt$al`A;itateEdeauna3NuSi4Kl-rAdatEi%ascAReSteWi5Nsc%mRt.aduc<e|Ti)reLa}i^fic<ul$g:AFe;Ti%i/nsformA+at`mite;portEs/tament;t2NeabA5Na%cA%z3Jbui6Ma6He6Mt`ri=lePc4Ne&mRi4
Lut6NA{e(ul3Ki%a:leaRzeciPnFul`rile/zeSte=i&sc:iGt.ibunal/coul/miTi5Ns&t<AHe|mPst;A`eTe]upA_ele:ul1Iu.rA^cA_a/nul2Nturor!v[ylerBuSA2Ma]i/leOoarA3Mr.urel:inTA-au[ciSi/d:AFe;rea/gaS<ul3Ns_A/ziChCiTi.mitoare(r2Nt3NA%m3NaRTi:m4Mt3LeCl.ei#timA5MaUele&iiGulNm#anRARe.brA:aRela]ple%ut1Fn2LaOchiul=e]dA3IeFva2Mei3Nle3Nori]ghiile]ic_A^formA3Ni^tate=aRe/vers=itate?atea)ulOor]tDu3Mi3Ll!rASte;iEscOQt:A#a#cA^a%t.eche;i<le#genTA;t.i^aS2MmA:reSte>i<sc`i(tRtoareYa?leVrulEa%re%t$eRazA:le_zi.s^ul-scat-til0IvA2Kd.i]rsat^ul2Kzut-QnAtoare$d:ARut$tRul$zare#rful3NstAGa1Ha.caRnTA{a2NdA.liza$oare|a:reazA.n#rAEa.sele!eSti`le2NTiDche;a4Ni;ul/inii;ulOdeFTi4Ma4MmFre<a]gas2Ki2MniFTi%m4KtDrde$ific)A>m|aTi*t_i^suri/ziOst:e&a2Lzi!i2LaTA4Ka^tA#ctimA<e:or<ia=e#deo.e/TiGi;le2Mi3NtoareGrVul2Ln3MAEa^centPde`cA{at3Le%ri3MoRvat|A$ul/zi.olenTA=a{t]rusulOs$at/e%le:z$ul#tezA#u#zitAUaVt`eazA(z|e-oStriDastrAVe#ceRa^i2IiPa:iFmEe^nTA]luntar2Km2KrPbA4Na4MeSte7Mi&a<m6NscA5Lsc4MiGTi5Nm&nd5MtOstru]t/at]uA-rAjitoare2NeTi3Ja4Iu3JiEm4Ne5Na:uri3Mo4MdatAEun`ul.oia&m2Lut,walter#shington!eekend!ill:iam!ow,yanni[eah.niCork#uMzApadAUa.u[QmbeSte;t{ul%it!ahAr!boarA$r:ul.ura&t1Nece/i.ro]u!gomot<ul1Ki#ar:e`le%ulDcEe_m3Ni]d^ul2MleRiFle/nic#ri2Ms2LuaNonA$a]ologicA]ri-vonuri"""
DATA_EN = """0Da!ah-bandoned#ility2Mle2HoutPveOroad.sence;tEolutely-ccentFpt(ed%ss3NidentPordingRunt$usedDrossDt/ed$ingRon<s_ve`ity/or/ress^ual6Mly!damOd/edPress]mireRt;ted]opted.ult.vance|d&tage^entureEice_se(d-ffair<sPord2Mraid$ica2KterGnoon`wards1Kgain5Mst2Ne^ncyRt/s2MoDreeUd;ment1Nh2Nead]h[id.m2Nr/planeRort-l.an$rm]bum.cohol]ert$x.ice^en3Nve2HlPowUed2Mmost2Mone4Ng2LreadyEight2MsoOthough2Kways1JmOazing.bulanceDericaJn*sOong$unt.y1In#cient2Fd/y#gel%r3NryOimalVs.n/a^ie^ouncer:ying2Lother2Mswer(ed{ing(s.xious2Jy3Nbody3Mmore3Mone3Kthing_ime3NwayFhereNpartUmentOologize{y#parently$ear<ance<ed(s$lauseRe&s_ication`ed:y$ointmentPreciate:oach}ing`priate`ve.ril1GrePa_sEn't.gue_ing%mentOm/edPsPy2Lound.ranged$est(edPiveHd`ingDt/hur$icle%st1Hs#hamed#ide2Lk3LedEing/sDleepDs$hole/istant$ume_re1HtDe.mosphereOtack<ed/empt%nd{edGtion/itude/orney/ractive!udienceOnt#stralia]thor<ity^umn!vailable.erage#oid-w#ake$re3Ky#esome#ful]kward-ye,babe/ies3My2Jck:ground2Ld$lyDg/s.lanceEl%s#nd/gEkOr$ely/king.seRball%d:ment^ic;ally/ketballPtard#th%room^teryRle1GeOachPr:d_s^stEt_en:ing3MutifulUyDcame4Juse3Nome(s&ing2Md$room]ef3In/pingEr2Kfore#gEanPinUning;s^un.have&ior3Nind2Ling;s2Llieve)d)sPl$ong(s_ved%w/tOn/ch^efit]rlin.sideVs3LtDt^rayed3Kter_y3MweenOyond-ibleOcycle2LgPger&st#keDll:ion:s%yOrdRs$thGday2MtEch$e/ter1NlackPme.eeding:p/ss`ed$w#ind.ock3Nod&yPw:ing_sDueNoardEtOb/by.dies3Ny#mb.ne:s2Lok4Ns^m/ts.rder$ed$ingEn$row<ed2Nss3Mton2LthRer{ingPtle{s%om2Nught/nd.w/lDx/es2LyPfriend3NsNrain;s^nch:d$ve/zilOead4NkGfast&ing;s%th(e(ing.ian/deRge^ef$ght$lliant3Mng&ing&s^tain%ish.o3NkeGn3MtherWs3NughtPwn.ush-ucksOddyOildGing}sRt]ll%et%shit#nch#ried$n%ed%ing/st2Ns/h3Miness3Ny2Ht/t:er%on2My$ing1IyDe,cabOke.lifornia3Kl4LedFingRsEm2LmeFra{s$p:aign2Gn3K't/ada`ian/cel&r/dy3Mnot]p$able$italEtain_ured2KrPd%s3Le_d%er4NfulWly_less%s^l^pet$riedFy&ingPs^ter2Mse:sPh/t%le2Nt3Nch$s2NughtEse&d`s]ve-elebratePl#nter:ral`e%ury.remonyEtainJly-hainRr`man$llenge/mpagne3Mnce<s4MgeHd(s;ing_nel$racter~sRge<d<s:ity:lesUie:ming/se/t_ter|ing#eap_ted;ing3Nck&ed;ing^er&ing&s%se/f^rry/ss:t.icagoRkenPef3Mld&hood5MrenPnaRese#ocolateEicePose/se;n#ris&t<ianHmas]uckUles{ingPrch-igarette~s.rcle:umstances.ties_zen|s3My.vil-laim`s_re3Nss;es;roomDean;ed&ing4Nr`edUly;s$ver#ient{s/mate:b;ed`ing#ock3NseGd&r;s;t:ingEthes`ing^ud;sDub^e!oach/stPt#de2Nffee]in_cidence2Mld/lect=ionGge$onelRr`s_ur2Ime4Ms^fort)able3Ling$mand)er:ent:it(ted>eRon_unication)ty/panies6Ny;red:etition:lain>ingUeteKly<x&icatedFuter>s]ncentrate;rnWedVt$dition?s/ference;ss:idence}t%used$gratulations/nected=ion^science_equencesRider*ed>ing_tant}ly;ructionPtact_ent;stRinue>d*s%ractGol^venientUrsation%ince*dOok:ed_ie<s&ng3Nl#p$s$yOrnerPrect.sEt:s.uch3Jld;'ve5Nn't/ncilRt;ing&ries6My`y3Nple$rage4MseRt$sinOverUed.w/ard-rack$p/sh3Nzy#eam%te(d;ure$dit$w#iedPme`s%inal/sisOoss;ed`ingPwd`ed_n.uel/shDyEing!ultureOp.re/ious/rent|ly^se]stody`mer>s2NtPe/ting,da2MdEdy.ily#mage{d3Nn.nEce%ingPgerHous/iel$nyOreEk:nessPling#taEe$ing2Nughter}s.vePid.wn2Ky3Ls!e2Mad^f3Nl:ing^n3Nr3Mth.bt.centPide6Nd
Fsion>sOep%ly.feat:nd;sePinitely.gree<s#licious:ver|ed|y.mand]nied^tist/yOpartment$ends/ressed.scribe/ert&ve=s/ign{ed%rePk/perate:ite/tiny%roy)ed.tail(sPective:rmined.veloped=ment/ice%l-iamond/ry#ck$tionary2Id3Kn't2Me3Nd/s/tOfference8Mt4Nicult~ies?y.g2Nnner.rect<ion<ly(or^tRy.sappear+ed(ointed:ster$coveredRuss=ed=ion$ease/gusting/h%es$tance{t:rict#vorce=d-na1Go.c3Mtor(s^ument>s2Kes4Ln't2MgPs.in4Kg.ll:arHs2In't3Le2Lor%s#ubleFt2Jwn:stairs_town.zen!r]ag:on^ma`tic$nk$w_er:ingDeam;ed;ingUsEssUed/w2MinkGing&s3NveUr;sFingDopRped$ve#ug%sEnk#y-uckOdeOe#mb^p2Nring.stOtyNying0Meach#rPlier4Ny/n_ed$s3Nth;quake.se$ierRly$t3My2LtPenEing$s-conomic<y-d.die.ge#ucation!ffect{ive<s$ort<s!ggPsNhCight2Nther-lected;ion;ric>ity^phant/vator_en]izabeth2Lse-mail.barrassed?ing#ergency#ily.ma.otional]peror/ire/loyeesPty1Mnd$ed$s#emiesRyPrgy.gaged{ment$ine{er$land4MishDjoy&ed;ing2Lough#ter&edPire<ly/rance]velope/ironment-qual/ipment!r.ic]rorNscape(dOpecially%ranto]sential.tateNurope<an-ve3Kn4Ning%t;s&ually3Kr4Ky5Mbody5Lone5KthingUwhereOidencePl[x.act5MlyPm%inationRpleOcellentFpt/hangePited&ing3Nuse#ercise.hausted#ist;ence`s^tDpectVed(ingRnsiveFrience?ed<ment;tElain=ed&nation:osion/ress=ion#tra;ordinary%emelyCye3Ms0Mface_book:s3Nt%ory%s#ilRed%urePr:ly$th#keDll%en%ing:s/se#miliar<es5LyEous#n/cy^s$tastic2Mr$m_er.shion3Nt%erOt$e3Kher<'sDultOvorGite_urite-biCear.d^eral#ed3Ll4NingWsRsEt2Nll%ow3Nt#male.nce.stival.ver2MwNield`s.fteen_h:y2NghtUingEureVd{s#le:s$l%edEm:sOnal5Nly:ncial3Kd%ing%s3Le$ger(sEish6Ned2NreRd$m3KstDsh%ingOt2MveOx$ed-lag$t]esh/w]iesPghtDoor$werHsOy$ing!ocus#lksElow(edVing{s.nd2ModEl:ishPt%ball2GrPce&d;sPeign%stRver3MgetFiveFot(tenPm:er_s^th%une:yEward#ught3Lnd3Nr:th.xNranceRk`ly.eak/d3Ne%dom_ze3MnchPsh#iday_ge3Lend(ly6Ls)hip/ghtened2Iom3Nnt/zen#uit1Nuck:ed%in6Ng]el2Nll:y2Mn/eral3Nny.rniturePtherDture,gain2NmeRs.ng.rage/bagePden^yOs$ps#te^her{ed2Mve#yCeneral=ly<tion;ous$ius^tle(manWenOorgeDrman{sVy2Ht3Ns3Lting!host;s-iantOft_s2LrlFfriend4Ns2JveFnRsEing1NladEssUes]obal^ry/ves1Ho#al2Ld$damn/s2Nes.in4IgOld:en$f2Mne3Kna2IodFbye:ness:s.rgeous.sh2It3NtaRenDvernment<or!rab:bed$ce/de_uated$ndUfather&ma(other;pa:t;ed/ss/teful/ve^y2Keat;er(st/ekRnPw.oaning&sPundFp`sPw%ing%n#unting&s-uarantee%d;s2Mess%t&s.idePlty$tar2Nn$s_hot2Ly3Ls-ymBha#bit2Id$n't2Nir2NlfPl2Mnd%edFle4Ns&omeEg%ing2Mppen6LedHingHs_ierUness4Ly2LrdRerRly$m$ry2IsPn'tOt3Ne:d%s2Gve4Nn't3Ming1FeO'd$ll3Ls2Mad:ache:ed:ing%sElth(y3Lr4LdRing4Mt;sPt$ven:ilyRy]hOld/en3Ml4Mo3JpFed:fulRing:s#nry2Hr3He:'s$oEself2Ky1Mi.d$denPePing2Mgh%er`st:ly#ll2Hm3Mself.re%d2HsEtory2Nt^ting[mDm-o]bby2MldRing_s$e$iday|s$y2Kme_sRworkDnest(ly{yFyPor:ur.ok2Mpe:d:sPing.rn$ribleEse&s2Nspital2NtEel2Nur4Ms3Kse&s2HwPever-ugPe2Mh2Nman`ity&s^orDndred=s$gFry/t_er:ing2Nrry3Nt_ing%s2Nsband0Ci1M'd2Lll2Im2LveCce[d2LeaRs^ntityOiot1Hf-gnoreNll/egal$ness-mage:inationVeOmediately.portance8MtFssible$ressed=ion>ve:ove1Fn.cident/luding/ome/rease&dible~y#deed:pendent$ia;n:stinct:vidual/ustry.fluence^ormHation{ed#juredOnocent.sane3Nide_st{ed/pectorEtead:ructions$ur
ance.telligence?nt%nd<ed;tionRrestKedKing}s&national(et`rupt&view3Ko$roduce?d.vented%stigation/itation&eVdPolved-ron1EsOland2Ln't#sue;s1Et#'ll3Js#alian%y2MsPelfBjack%et%sonOil.ke.m$esOne2Npan5Nese.son]zz!ealous.ff]nny.rk/ryDsusNim$my1Lob$sOe2Nhn%ny_sonDin:edOke:s/ing.nes]sh#urney#yNudge#ice]lia_e/yOmp%ed.ne/ior.ry2Hst%ice@karen#te1Keep%ingRs.lly#nDpt.vinDyPs!ick%ed2NdPding3Ns2Mll4MedUrRing.m2Lnd:a:ness%sEg:domDss%ed:ingOtchen[nee:s3LwOife#ock;ed;ing3Gw%ingRledge4Nn4Ms-yotoZla.b^or#ckOdies3Ny#idOkeDnd_ed3NguageXsDrge;r;st/ry2Kst2Mte%ly4Mr:st^inOugh&edGingGsUter^ndry/raDw/sPyerOy.zyNead%er:ing:s3NrnGedUing3Nst3KveUs4Ning]cture#d#e2LftOg/alPs#nd^gth]o2Nss%on<s2It3M's^s3NterVs%ingOvel!iar.bertyPrary#cense2NePdPs$utenant2Kfe$t2Nght;ning&s2HkeFdRly4Ns]ly]mit]nda3Ne%s^k.on.ps.saEt4Len(edVing.terally{ture3Jtle2LveFd4Ns3Ning-oad/nOcal:ted;ionPkRedOndon$ely3Kg4Ner2Jok4Med4Ling4Ls$seDrd2Nse:rPing$s3Mt2KtPs#ud^is2JveFdRly:rFs/ingOw$er!tCuckFy/y]ggage]ke2NnchCyingBmaDchine|sDd$am;e3Ke#gazine$ic]id$lPn#jestyPor2Jke4Ms3Ming#le#ma2Jn^'s$age(dVr/ner<s3Ky#p.rch$ia_ePkRet:sPriage5MedFy^s/tin3Jy4N's]sk/sEterOtch$e:rial/h:ematics/t4Mer(s#x2Ky3Lbe$or1Fe#al:s3KnRing4NsFtPt.dia%calUine2Met4Ning#mber(s/oriesUy2Mn/talRion=ed.rcy^ely/ryOssFage|s2Mt/al/ers/hod.xicoNichaelDddle$night2LghtOke]leRs$itaryEkElion=s2Lnd:s3Ne^imum%ster^or3Nute6Ms.racle$ror.serable3MsFedFing&on3Ntake=nWs:er]x/ed!m#m-obile#del%rn2Mm3Nent<s$myOnday3Key/key^sieur%ter3Nth5Ns#odPn2Jre3Lning2Lst:ly2Lther{'s{fucker^ionOuntain*s/seEth2MveFd:ment:s3NieUsFng1MrOs1JuchOmDrder(ed=r#seum3Mic`ian3Kt_'ve1Gy2Mself^terious<y,nah]il#ked2LmeRdRs.ncy#rrator_ow.sty#tion(al{s%vePural=lyUeCear:byRlyOcessary$k2JedFed4Ns.gative.ighbor*hood>sPther]rveRous2Jver2Kw3Ns%paper?s2Lxt1Lice$k2Kght`mare;sOne1Go]ble3ModyOiseDne$sense.on.peOrPmal<lyPthOse2Gt$e:s3KhingPiceVd#vel2Iw/adays$here-uclear2Mmber(s#rse#tsMo'clock-bey.ject#viousWly-ccasion/urred#ean]tober-dd1Ef2JfEer&ed`ing3MiceVr=s;ial2Mten1Ih.hNil1Lk2Jay1KldPer1Gn2Lce2He$'sEs.line3Jy#toNoh1MpenRed%ing:s$rationDinion|sOportunity:site]tion{s1Jr.ange2Nder&ed&s/inary]ganization#iginal-saka1Kther5Ns&wiseNught2Jr$sRelves2Ht3Nside/ta1Jver!wOe2Ln/er/sZpack:age_ed#ge_sDidEn:ful%t&edUing$r.l/ace/e.nic/ting%s.paEer&s#rdon3MentsPisEk:ed:ing3Mt%icular?rly;es%ner%s4MyDssFed;ngers:ing;on:port3Nt#th_etic/ienceVt=sOul2My$ingCeace#n/cil/ny2Jople#r/centEfect)ly_orm=anceEhaps$iod$mission3MsonVal}ity>ly_uade]t/eRr[hil2Mone$to`graph&s.ysicalNiano2NckRed:ing/nic3NtureWs.eEce&s.g.lls/ot.nk.pe.ss_ed#ty#zza1Llace`dUs/in3MnFeUt%nedUingRs%t;s/stic/te3LyRed&r<s4NingRs.easant5Je(dUurePnty#us!ocket.em/t2Nint`ed&s/son2Mlice(man;y:te&ical|ian)s]nd#ol3Nr#pPular(tionOsition<ve/sibility6Nle)yPt.t/atoes^ential.unds/red]verty2Nwer&ful;sNractice^ise$y.eciousPfer$gnant$pareWd{ing/senceHt|sFidentRs&ure$tend=ed|ing4Mty/vent:ious}lyDice&s/de/est$me$nce(ss`ipalPson<er>sPvate$ze2Mobably4Llem7Ns$cess^duce<t=ion=s$fessionalWor_it$gram&essPject3NmiseWd=s$of/per<ly(ty%osalPtect=ionEudPve`d:ide|dCublicDllRed:ing.nch/ished<me
nt.rePpose/seOsh:ed_ing2Kt/sPting,quality/rterOeen3Mstion8NsDickGlyEet;lyEt4Me,rabbitOce/helDdio2Nin%ing:sPse&d2Nn/g:e.re:ly.t$e3Nher]w#yNeachUed_tion3MdFing_s4My3Ml%ityUzeWd4Jly3Nson<able(s]call/eiveWd:ntVly$ognize?d:mmendRrd(s2Nd.fuse(d]gion$ret/ular.latedUionshipRx/ease=d/igion=us^y#main<ed<s_rkable3Lember>ed$ind<s/ove<d#nt]pair$eat^lace:yEort<ed|r<s/utation#quest_ire|d|s.scue$earch^ist^ourcesPpect_ond<se)ibilityYle3NtFaurantPult(s]tiredEurnVed.venge/olution]ward!iceEh%ard^kOdEe$iculous:ng2Ight&sOng%ing%s#se^ingPkDver1Noad.b/bed`ry$ert^otOck:s.ger#le$l]man;tic$e#of3Lm:s.pe#se:s#ughEnd^te.w.yal!ude.in%edOleRs.mor2Mn3Nning$s.sh/sia(n-yan@sacrificeDd2Nfe_ly%ty2Jid^ntOke.lad%ry/e:s$tOm3Le.n/d%wich/g/ta#rahDt$isfied$urday]uce2NveRd/ing2Lw2Jy3Ming3Ms-careGd:yOene#hedule3Lool{sOience;tific|st?s]offs/re/tt]ratch/eamVing<s:en:w;edCea^nPrch{ed<ing$sonEt:s2Mcond(s3Nret(ary(s/tion^ureUity2IeEing/k3NmFed4Ms3Ln$s.ldom$f:ishEl%ing2Nnd:ing/ior3Nse:itive3NtFence*s.parate#rgeant/ies4NousWly$ve;dRice=s2Nt^s/ting%le<dDvenFral`eDx/ual/y-hadow$ke3Nll$me$pePre`d%p2He3N's/ep^lf/riff#h]ift^neEp:sPrt3Mt.ock;ed/eFsEot&ingPpRpingErt3Nt:s3JuldV've(er}sHn't_t&ing3LwRed&r%ing:n%s2Nut#y1Nick2Nde:sDghsRtEn:al%ed:s#lence&t$ly/ver#milar/onEpleUy.n3MceEg%erRingFle/k2Lr2Mster(s2Mt/eEtingEuation2Nx#ze[kiing/llsPn^rtOy[lave2MeepGing;y$pt.ightly/p:pedOowRly1Nmall;erPrtOell;sOile;d:ing$thOokeRing-nakeDow1Ho#ccer$ial%ety/ks]fa$t]larPd%ier)s/id$utionPve;d2Jme4Nbody:day%how4Lone4Jthing;ime8NsFwhere2Ln3Ng%s/s2Lon%er2KrryEtOul3Nnd;edGs$p/rcePthCpace/inPnish$re2Leak&erGingUsEcial;es`ficPech%d/llEnd;ingFt#irit{s^te#litOoke&n/rt&sPt#readPing.y!quare[t#aff$ge$irs3Nnd`ardGing&sPr:ed:ingRs4Mt5MedUing&sEte;mentGs4Nion3LyRedRing:s]eady%l;ingEp:ped:s$veOick3Kll.ockPleUn$machPnePod3KpFped`ing:sEreRiesRm4MyDraightFnge)r}s3Neet(s%ngth:ss$ikeEong<er/uck_ggle]ubbornPckEdent7Ns%ied<s;o4NyUing3Nff3Npid#yleNubject#cceed=edUss)ful3Lh/k_s#ddenVly.e#ffer<ed(ingOgarPgest)ed=ion#icidePt:case_sDmmerDnPday#per`ior;market/per:lies;yRortGse7Nd2Kre%ly/face$geryEpriseKd^render:ounded$vive=d.san$pect:iciousNwear:t;erEet&heart;ieDimRming/tch#ordCystem0Ntable.il2Jke4NnFs3Ming.lent{ed3KkFed4Ling%sPl:er]nk#pe#rget#skPte;s#toebaOught.x^es$iCeaEch5Ner=s&ing3Nm/rRs.chnology.dOethOlephoneRvision3Jl4Ning%s.mper<ature:le2Nn/dPnis^se^t.rm%sErible=y`ficDst:s#xt!h2Jan4Kk5Ls3Et4L's2Ce$ater^e3Kir3Jm_eRselves3Jn$ory3Hre5M's;fore3Kse3Hy:'llGre`ve.ick$ef/n4Kg5Ks4Ik5MingGsPrd:styRty3Fs.omas3Kse/u4Ngh6Kt)sRsand*s.reat<ened4KeRw$oat4Lugh=outFw;ing;n.under^rsday/s.yNicket(sOe/d.ger$htDll.m3Ie4Ms#ny.p2Nred:s]tle1Do.ast2Kday;'s2Lgether#iletOkyo2Kld2Fm3M's/my3Lorrow]ne$gue3Might$y2Jo3Lk^lsDp#talUlyDuch;edPgh/r#ward(s^el:r3Nn.y^s[race%k$dePffic3Nin;ed&ing$nslate~d>ion/p:ped/shPvel<ing.easure%t&ed;mentEeRs#ial$ck3Med:sEp.oops3NubleOuck3Me$ly^nk3Nst;ed3Mth2Ly3Ling-uesday]ne^nel.rkey3Mn4Ned%ingRs1Nv-welvePntyOice^ns2JoNype^ical,ugh#ly1Lh1Nm#brella-nable.believableDcle^omfortable2Mder5Lstand?ding~dsWood#fortunately.happy.iform$on/que/tFed$verseWi
ty]knownOless/ikely2Mtil.usual1HpOonOset$tairs-rgent1Is2Le3Ld$ful$less/sDing#ualGlyMvacation.in.lley/uable%e#n.rious-egetables.hicle]rsion3Iy!ictim<s:oryOdeoOewOllage.olence<t.sionFtUed;ing`orsCoice;s#te0KwaitRed4MingDke2MlkFedFing:sEl%et:s/ter2Nnna3Ht4Led:ing4Ls2NrPm/n:ed:ing^rant2GsPh:ed:ing=ton3Nn'tPte;d:ing2MtchUedGing3Mer.ve:s2JyPs1Fe.'d3Nll3MreEve#ak/lth$pon(sErFing:sEther.bsiteDdding2MekRendFsOightPrd2Nlcome3Il2Knt2Ire%n't#st_ern#t1Fhat4M's4Never.eel3InRever3Jre&'s;verEther2Lich3Lle^stle3Nte2IoP'sEa$ever3MlePm/o^reEse2Iy!ide2Mfe#ld3Hl:iamUng2NnPdFow(sEe/gs/ner:ing/sPter]re.sdom$e3Mh:es.tch3GhRin4Lout$ness|es!oke.lf2Lman3Nen2Ln3M't3Nder(edHful(ing#od%s2Mrd4Ns/e3Jk4Ned`r(s4Ming4Ns3Lld^nEried<s4My;ingEseRtEth2Iuld;'ve5Nn't/nd;edDw1Nrite&r;sFingFten2LongEte,yard1Ieah3Lr4Ks.lling%ow#n#p2Js3Mterday2Lt!oDrk2DuE'd4Nll4Kre4Nve3MngUer3Gr4Ns5Lelf=ves$th,zero[one.o"""
PAIRS = """ISi|ETine
ITi|Cva
Ii|Dva
ImbrAcat|@ca
Imi|Eva
ImpreunA|Cca
In|EaceastA FfaTa FfrancezA Glimba GviaTA GvQrstA GenglezA Hseara HdimineaTa IportughezA ITara KcapitalA KrQu LcauzA LseamA
InTeleg|Cgermana
Inainte|Cca
Inalt|Bca
Si|JajutA Jaceasta KsiguranTa
Stia|>cA
Stiam|>cA
Stie|AcA
Stiu|@cA
Stiut|>cA
a|Afost Cspus Dlot Dgood Dlittle Enew Efew Fvery Flong Fgreat Fman Fbig Gbit Gweek Gcar Gwhile Gbad Gdus Gbook Hsmall Hchild Hlarge Hdoctor Idoua JInvATa KvA
aSa|BcA
aSteaptA|Bca
able|=to
about|Bit
absenTa|?sa
aceastA|DcamerA DcasA DproblemA EdimineaTA FsearA
acest|FrQu
afraid|?of
agree|>with
aici|Gca
alb|Aca
all|Athe Dday
an|Chour Cold
and|Bmary
any|Bmore
ar|?trebui GIntQmpla Iexista
arATi|@ca
aratA|Aca
are|@you GimportanTA
aren't|?you
as|Aa Csoon Cwell Epossible
asked|@me Amary
asta|Ica
at|@the Call Chome Dleast Donce Enight
avut|DSansa
away|Afrom
back|@to
be|Ba Dable Dhere Elate Ehappy Fcareful
because|@of
began|>to
better|@than
bine|Fca
bought|?a
bun|Fca FsimT
bunA|DdimineaTa DprietenA
but|Ai Bhe
buy|@a
by|@the
cA|Eva Jaceasta
cQntecul|@Asta
ca|AsA
came|@to
camera|Csa
can|Ayou Cdo Cbe Dspeak
can't|Cbelieve
care|?of
cariera|>sa
cartea|Daceasta
ce|ForA FvQrstA GlimbA HvA
ceea|=ce
cine|Cva
come|Ato Bback
comporTi|>ca
could|Ayou Bnot
cred|=cA
crede|>cA
credeam|=cA
crezi|>cA
crezut|=cA
cu|Dtine FapA FmaSina Hbicicleta Inoua IvQrsta
cum|EvA
cup|>of
de|GmuncA Gtine HviaTA ImQnA JzApadA Jdata JdimineaTA JmuzicA JcasA JmaSinA JsAptAmQnA JStiinTA KvarA KiarnA KsearA LfatA Mpersoana
deal|?with
decided|>to
devreme|Asau
dezvoltarea|@sa
did|?you Btom Bnot
didn't|Bknow Bwant
difference|>between
din|Bcauza GcasA GgurA HTara HfaTA
discursul|?sAu
do|?you Bit Bthat Dnot Eanything
doar|Eca
does|@not Atom
doesn't|Aknow Bwant Blike
don't|Aknow Bwant Bhave Cthink Clike
drumul|CAsta
during|>the
e|Hca
each|>other
el|Fva
end|?of
era|Gsingura
este|Hca JdiferenTa Jlimba Jora Jsingura MsiguranTa
even|Athough
every|?day Bmorning
exact|Aca
fac|@asta
facA|?asta
face|Aasta EfaTA Eca
familia|Dsa
feel|@like
fel|Bca
few|Adays
fie|Dca
fiecare|CdimineaTA
find|Aout
first|@time
fiu|Dca
fiul|BsAu
for|Athe Aa Cme Dhis Ethree
fratele|BsAu
from|@the
front|>of
frumoasA|Cca
full|?of
gave|@me
genul|AAsta
get|Dmarried
give|@me Bup
go|@to Cout Chome
going|>to
good|Bat Cidea
got|Aa
had|@a Ato Cno Cbeen
has|Aa Abeen
have|Ato Aa Cbeen Dany Dno
he|Ais Awas Chas Dhad Ewill Edidn't Edoesn't Esaid Fwent Fwants
help|Ame Bus
high|?school
him|Bto
his|Eown Ewife Efather
hotelul|?Asta
how|@to Bmany Bmuch Bdo Bdid Blong
i|Bdon't Chave Cwas Cthink Dam Dwant Dcan't Dknow Ddidn't Ecan Ehad Ethought Eneed Ejust Ewill Flike Fwould Fcould Fsaw Fgot Fhope Fwish Gtold Glove Gnever Ghaven't Gshould Gwonder Gfeel Gcouldn't Gwent Gheard Gcannot Gwon't Gknew Hfound Hwouldn't Hwasn't Hbought
i'd|>like
i'll|Abe
i'm|Anot Bgoing Csure Csorry Dafraid Eglad
i've|@been Agot Anever Bever
ice|?cream
if|?you Ai Bhe
in|@the Ba Dhis Dthis Dmy Dboston Flove Ffront Fjapan Forder
interested|>in
into|?the
is|Ba Dnot Dvery Ean Fgoing Fstill Gquite
isn't|Ahe
it|Ais Bwas Fseems Flooks Fwasn't
it's|Aa Bnot
jocul|AAsta
kind|>of
know|Awhat Bhow Bthat Cwhere Dwhy
la|DScoalA Eora GuSA HvQrsta HcinA Hcasa IgrAdina ITarA JsalA Jalta KduS
last|@night Btime Byear Bweek
less|?than
let|?me
let's|Ago
like|@to Ba
limba|AenglezA
listen|>to
live|?in
lives|?in
locul|DAsta
long|@time
look|@at
looking|?for Aforward
looks|?like
lot|>of
love|Awith
lucreazA|Aca
lucru|Eca
lui|?tom
luna|Caceasta
mA|Fva GaSteptam HajutA
mQine|Cva
maSina|Fsa
made|@a
make|Aa Bsure
mama|Dsa
many|Bpeople Ctimes
mary|Fva
may|Abe
me|Bto
might|?be
mine|Fca
moartea|Bsa
more|@than
mult|Fca
munca|Bsa
must|@be
my|Cfather Dmother Ebrother Ehouse Esister Elife Efriend Eparents
ne|Eva
need|?to
never|Cbeen
new|Byork
next|Aweek
no|Aone Cidea Cmatter Dlonger
normA|?IntreagA
not|Dgoing Esure
nu|Ci DmA Iuita JlAsa Ksta LTine
o|CsA FpersoanA FmaSinA FlimbA FproblemA FdatA GnouA GcasA GpisicA GsingurA GfatA GsAptAmQnA GorA HTarA HtreabA IinimA IviaTA IbicicletA IfiicA IfurtunA ImQnA IechipA IlunA IprietenA JcamerA JslujbA JfirmA JmamA JdorinTA KadresA KultimA LprimA
ocupat|Cca
of|@the Dhis Dmy
off|@the
old|Bman
older|?than
omul|CAsta
on|?the Chis Cmy
one|Aof Bwho
only|Aone
or|Anot
orice|BlimbA
out|?of
over|@the
pare|@cA
part|>of
pe|EmasA Ftine GsAptAmQnA HlunA IfaTA Jdata
pentru|AcA Dtine
peste|ErQu
piece|=of
place|?sA Emuzica FzApada Fciocolata
play|Btennis
poTi|?sA Dda
posibil|Aca
pot|?sA
prietena|Bsa
prima|?datA
principala|?cauzA
propria|@sa
propriul|?sAu
putea|?sA EIntQmpla
rAu|AcA
repede|Dca
rezolve|>problema
right|@now Baway
rog|?sA
romanul|@Asta
sA|CmA FvA HvinA Jintre Ltai
sAptAmQna|Aaceasta
said|Athat Ahe
say|Athat
se|Cva DIntQmplA DaflA DuitA FterminA GschimbA IcQStigA
see|Ayou
seem|>to
seems|?to
she|Bis Bwas Chas Dhad
should|Abe
shouldn't|?have
sigur|>cA
so|Bmuch
soTia|Asa
soon|?as
sora|Dsa
spart|Abanca
speak|@french Benglish
spre|AcasA
spun|?cA
spune|?cA
spus|>cA
stay|Ahere
studiez|Bfranceza
such|>a
sunt|Gca Jsingura
supposed|=to
tQnAr|Aca
take|@a Bcare
talk|?to @about
talking|?about
tatAl|AsAu
te|Fva
tell|@me @tom Ayou
ten|@years Aminutes
terminat|Btreaba
thank|=you
that|Bhe Eshe Emary
that's|Anot
the|Fsame Fworld Ffirst Fdoor Gway Glast Gonly Groom Gtruth Gbest Gmost Ghouse Gproblem Gparty Gtrain Gpolice Gcar Hother Hbook Hmeeting Htable Hboy Hnext Hbus Hstation Hwhole Hend Hnews Hcity Hwindow Hstreet Hsun Hdog Hteacher Hunited Haccident Iriver Ihospital Iweather Ipark Iroad Ikitchen
there|@is Aare Bwas Cwere
there's|@a @no Anothing
these|Bdays
they|Bare Bwere
think|Atom Cit's Cabout
thinking|?about
this|Ais Ebook Emorning Fafternoon
those|@who
three|Ayears Bhours Bdays Btimes
through|?the
time|Bto
tipul|?Asta
to|Cbe Cdo Dgo Dget Esee Ehelp Fmake Ftell Fsay Ftalk Ftake Fcome Feat Fwork Fbuy Fboston Gleave Gfind Gstay Ggive Glive Gspeak Gask Gschool Gplay Gmeet Glearn Hread Hhear Hstudy Hbed
toatA|BviaTa
told|?me Atom Bmary
tom|@a Ais Cwas Dhas Ddoesn't Ddidn't EsA Eva Eisn't Fwill Fsaid Ftold Fhad Fasked Fwants Gcouldn't Gseems Gknows Gwanted Gsays Gtook Glooked Gwasn't Hwon't Hhasn't LcAuta
too|Amuch
trebui|=sA
trebuie|=sA
trebuit|=sA
tried|>to
try|?to
trying|=to
un|IduS IpeSte IrQu
united|=states
up|Bwith
used|>to
vQrstA|Bca
va|DIntQmpla Eploua FlAsa Gcosta GTine
vara|Caceasta
very|Cgood Cmuch Cwell
voi|Dda Euita ElAsa Fsuna Gurma
vor|Eca ETine
vorbeSte|Cfranceza
vorbeascA|Bfranceza
vorbesc|Cfranceza
vrea|>sA Eca
vreau|>sA Cca
vrei|>sA Dca
vrut|Dca
waiting|>for
want|>to
wanted|>to
wants|>to
was|Ba Every Fborn
watching|@tv
way|@to
we|Bhave Care Ccan Cwere Cshould Dneed Dhad Ddon't Dmust Ecan't
we're|Agoing
we've|?got
went|?to
what|Che Cdo Cis Chappened Dare Ddid
what's|@your
when|@i Ahe
where|Adid
why|Adon't Bare Bdid Bdo Cdidn't
will|@be
with|Ba Ctom Cme Chis Chim Dher Dus Dmary
won't|@be
wonder|?if
worry|?about
would|@you Abe Blike
years|Aago Aold
you|Chave Dwant Dknow Dare Ddon't Dthink Ecan Eshould Elike Ewere Fcan't Fmust Fneed Fever Hshouldn't
you'd|?better
you're|Anot
you've|@got
your|Dfavorite
ziua|Esa"""
ENDS = "InvATM TiL aG aceaT aceastAV aceeaSiT altAU amQ arF areQ cAM cQndL cQtS caK ceS celeT cuM darM datL deR dejaN despreM eM eStiL elQ esteL fArAU faceQ fiecareW fostM iarK limbaW mQineR mareU meaS multAU multL nicioW oW oraS oriceU pentruM placeK poTiF poateI potH primaW prinS puteaF sAW sauK seS singuraT spreS subR terminatM toatAE tomR ultimaU vAzutG vaE veiG voiD vorbeSteM vorbeascAL vorbescK vreoU"
RULES = "Aciu Adui Ajit Alui Arbat Areas Areat Areti Arim Arui Arut Asari Asit$ Asura Atate Ateas Atest Atile Atise Atos Atrat Auta Azb Azus Azut Impru Inalt Inca Incep Incet Inch Incui Indoi Inflo Ingri Inm Inno Inot Inr Insel Intep Intre Intun Invat Qmpla Qndu$ Qnge Sai Sede Sedin Serp Snu Somaj Sti$ Stiin Stri$ Tia$ Tie$ Tiil Tinut Tioa Tion Tisa Tiuni ^Imb ^Impi ^Indr ^Inl ^Insa ^Inso ^Inta ^Intin ^Soar ^aSez ^amQna ^bunA ^cAla ^cQnta ^calA ^forT ^gAi ^gAti ^greSe ^mAre ^oTe ^pAca ^rAce ^rAst ^radA ^reTe ^tAie ^vQn aSi$ aTi$ aTie aTii aTil aTiu alAtur anAto anatA apAsat arAsi areaT asAri ascA$ atiSe bAtr bTin bdA bilA$ brAcat brAr braT cAldu cAlz cAm$ cAmin cArcat cArei cAril cAsato cAtori cQnd$ cQndu cQntar cQstig cTie cTii cTio cTiu caStig calT casAto cenuS citAri clAd crAri creSt cuTi$ cultAt dAuna dQnc depaS dusA dviS eInc eSec eSi$ eSin eSte$ eStep eTi$ eTii eTui eagA$ eanA ecAto enTie enTio eneS epAs eralA eranT erinT fAcut fAtui farA$ frQng gAtit gQnd$ gQndi gicA$ hiTi hrA iSat iSoar iStii iTi$ iTia iTie iTii iaSi iazA icatA icuT iinT imT impAra insA$ ioSi$ itAm$ itQnd ivitAti ivorT lAnui lAtit lAtori lQng lTi$ latA$ leagA liniS litAti mAgit mArf mAsu mQnca mQnes mTi mbiT menTi miSc moSte mparTi muTi mulTim mulTu nSel nStie nTei$ nTeleg nTep nTi$ nTia nTii naSte natA$ ncApat ndepA ndrA nducA neSte nesA nfrQn nitA$ nitAti nouA nrA ntAm$ ntQmp ntalA nuSa numAr nvAt nzAto oTi$ oTii oTio oaSte oasA oatA$ obiS ogaTi onaTi onalA onatA onunT oraS orbAr oritAti otAra ouAs pAia pAsit pAtan pQndit pTi$ pTii paSit paTan patA$ patQn peSt plAcu prAj pregA puSc pulaT pusA rAbd rAcie rAdin rArii rAril rAsar rAsf rAsp rAut rQnd$ rQndu rQnet rTi$ rTia raTio radiT ranTei raneSt raneT raspQ ratA$ rbAto rciTi reSte reTio reuS rieTi rinTa$ rnA$ ruSi sAnat sAra sArit sanAt sarbAt satA scAto scuTi seSt semAn serA$ sfaS sivA slAbi soT spQnd spreT stAp stapQ steSt stiTi sticA$ stinT strAdu strAnu straTi susTi tApan tAres tArile tAtes tAtil tAtit tQln tQrn taTes taTi tapQn tatA tiSa tialA tilA$ titA$ toreSt trAlu treTi tuitA uAsp uSi$ uTia uTii$ uTio uTite uaTi ucAtor$ ufA ugAc uieSt uinT ulaTi umAra umQna umiTi umpA unAta unAto unTi unatAti unoSt upTi urAto ureS urmAr uvQn vAtat vAzu vQnat vQntu veTi veliS vieTu vorbA zAp zQnd zaTi zamA zatA zeSte zgQ zvA"
TOP = ['de sA nu In Si cA', 'the you to it is of']

P = {"lm": 1.25, "dele": 5.95, "ins": 9.258, "trans": 5.75, "maxtap": 13.973, "acc": 1.0,
 "strip": 8.0, "auto": 2.0, "valid": 4.9, "native": 2.678, "accent": 1.5,
 "accent_valid": 2.1, "unk_valid": 15.0, "unk": 18.7, "user": 10.0, "space": 1.25,
 "spacetap": 2.5, "beam": 32, "backoff": 0.92, "ends": 1.048, "prior": 0.94,
 "accent_ctx": 4.5, "split_nv": 1.275, "gapnotap": 2.5, "three": 2.0, "oov_pr": 0.6, "oov_fin": 0.0,
 "amb": 3.0, "amb_acc": 1.0}
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

COMBO = "BCDEFGHJKLMNOPRUVWXYZ!#$%&()*+,-./:;<=>?@[]^_`{|}~"

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
 pairs = {}
 for line in PAIRS.split("\n"):
  if "|" in line:
   a, rest = line.split("|", 1)
   pairs[a] = [[_num(x[0]), x[1:]] for x in rest.split(" ") if len(x) > 1]
 G["pairs"] = pairs
 G["pc"] = {a + " " + x[1]: x[0] for a in pairs for x in pairs[a]}
 G["ends"] = {x[:-1]: (ord(x[-1]) - 79) / 2.0 for x in ENDS.split(" ") if len(x) > 1}
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

def _first(s):
 return s[0]

def _second(s):
 return s[1]

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
   if isinstance(dm, (int, float)) and dm < 0.5 and pr >= 0.5 and not noun and not _evidence(prev, e, state):
    margin = min(margin, P["amb"] - P["amb_acc"] * P["acc"] * (_marks(best) - _marks(e)))
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
  if lab in "aist" and (i < len(e) - 1 or lab != "a" or P["oov_fin"] > 0.5):
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
 prev = _prev(state)
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
