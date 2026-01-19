using Microsoft.Win32;
using PdfSharp.Pdf.Content.Objects;

namespace ApiScanner
{
    // In documentation, possible expansion of application. Not currently used by scanner
    public class documentClass
    {

        public static string _class = "";
        /*
        COOP - Cooperatives
        CORP - Corporations
        FIRM - Firms
        LP_LLP - Limited Partnerships/Limited Liability Partnerships
        MHR - Manufactured Home Registry
        NR - Name Requests
        OTHER - Other
        PPR - Personal Property Registry
        SOCIETY - Societies
        XP - Extraprovincial Registrations(Deprecated)
        */
    }


    public class CoopDocumentType : documentType
    {
        public static string coopDocumentType = "COFI, CONT, COOP_MEMORANDUM, COOP_MISC, COOP_RULES, CORR, FILE";
    }

    public class CorpDocumentType : documentType
    {
        public static string corpDocumentType = "ADDR, AMAL, AMLG, AMLO, ANNR, APCO, ASNU, ATTN, CERT, CLW, CNTA, CNTI, CNTO, CNVS, COFF, COMP, CONT, CORC, CORP_AFFIDAVIT, CORP_MISC, CORR, COSD, COU, CRT, CRTO, DIRECTOR_AFFIDAVIT, DIRS, DISD, FILE, FRMA, INV, LTR, MNOR, NATB, PLNA, REGN, REGO, RSRI, SUPP, SYSR";
    }

    public class FirmDocumentType : documentType
    {
        public static string firmDocumentType = "ADDR, CNVF, CONT, COPN, CORR, DISS, FILE, FIRM_MISC, PART";
    }

    public class LpllpDocumentType : documentType
    {
        public static string lpllpDocumentType = "ANNR, ATTN, CHNM, CNVF, CONT, CORR, FILE, LP_LLP_MISC, LPRG";
    }

    public class MhrDocumentType : documentType
    {
        public static string mhrCode = "ABAN, ADDI, ADDR, AFDV, AFFE, AMEND_PERMIT, ATTA, BANK, BCLC, CANCEL_PERMIT, CAU, CAUC, CAUE, CONT, CORR, CORSP, COUR, CRTO, DEAT, DNCH, EXMN, EXNR, EXRE, EXRS, FNCH, FORE, FZE, GENT, LETA, MAID, MAIL, MARR, MEAM, MEM, MHR_MISC, MHSP, NAMV, NCAN, NCON, NPUB, NRED, PRE, PUBA, REBU, REG_101, REG_102, REG_103, REG_103E, REGC, REIV, REPV, REREGISTER_C, REST, STAT, SZL, TAXN, TAXS, THAW, TRAN, VEST, WHAL, WILL";
    }

    public class NrDocumentType : documentType
    {
        public static string nrDocumentType = "CONS, CORR, CONT, NR_MISC";
    }

    public class OtherDocumentType : documentType
    {
        public static string otherDocumentType = "ADMN, BCGT, FINC, FINM, RPTP";
    }

    public class PprDocumentType : documentType
    {
        public static string pprDocumenttype = "CONT, CORR, CRTO, DAT, FINS, FNCH, HSR, LHS, MEM, PPR, PPRC, PPR_MISC, PPRS, PRE, RGS, RPL";
    }

    public class SocietyDocumentType : documentType
    {
        public static string societyDocumentType = "ADDR, AFDV, AMAL, AMLG, ANNR, APCO, ASNU, ATTN, BYLT, BYLW, CERT, CLW, CNST, CNTA, CNTI, CNVS, CONT, CORC, CORR, COSD, CRTO, DIRS, DISD, FILE, FRMA, LTR, MNOR, OTP, PLNA, REGN, REGO, RSLN, RSRI, SOCF, SOC_MISC, SUPP, SYSR";
    }
}
