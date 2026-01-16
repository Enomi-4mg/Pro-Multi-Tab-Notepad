; ==============================================================================
; Pro Multi-Tab Notepad - NSIS インストーラースクリプト
; ==============================================================================
; このスクリプトは Pro Multi-Tab Notepad のインストーラーを生成します
; 多言語対応（日本語・英語）、ファイル関連付け、エラーハンドリングを含みます
; ==============================================================================

Unicode True

; ------------------------------------------------
; インクルード
; ------------------------------------------------
!include "MUI2.nsh"
!include "FileFunc.nsh"
!include "LogicLib.nsh"

; FileFunc マクロの定義
!insertmacro GetRoot
!insertmacro DriveSpace

; ------------------------------------------------
; アプリケーション情報（ビルド時に動的設定）
; ------------------------------------------------
!define APP_NAME "Pro Multi-Tab Notepad"
!ifndef APP_VERSION
  !define APP_VERSION "1.6.2"
!endif
!define APP_PUBLISHER "EnoMi-4mg, Personal"
!define APP_URL "https://github.com/yourusername/your-repo"
!define APP_EXE "Pro-Multi-Tab-Notepad.exe"
!define APP_UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\ProMultiTabNotepad"
!define APP_REG_KEY "Software\ProMultiTabNotepad"

; ------------------------------------------------
; インストーラー設定
; ------------------------------------------------
Name "${APP_NAME}"
OutFile "Pro-Multi-Tab-Notepad-Installer-v${APP_VERSION}.exe"
InstallDir "$PROGRAMFILES64\Pro-Multi-Tab-Notepad"
InstallDirRegKey HKLM "${APP_REG_KEY}" "InstallDir"
RequestExecutionLevel admin

; ------------------------------------------------
; インターフェース設定
; ------------------------------------------------
!define MUI_ABORTWARNING
!define MUI_ICON "${NSISDIR}\Contrib\Graphics\Icons\modern-install.ico"
!define MUI_UNICON "${NSISDIR}\Contrib\Graphics\Icons\modern-uninstall.ico"
!define MUI_HEADERIMAGE
!define MUI_HEADERIMAGE_BITMAP "${NSISDIR}\Contrib\Graphics\Header\nsis.bmp"
!define MUI_WELCOMEFINISHPAGE_BITMAP "${NSISDIR}\Contrib\Graphics\Wizard\win.bmp"

; ------------------------------------------------
; インストーラーページ
; ------------------------------------------------
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE.txt"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!define MUI_FINISHPAGE_RUN "$INSTDIR\${APP_EXE}"
!define MUI_FINISHPAGE_RUN_TEXT "$(LaunchApp)"
!insertmacro MUI_PAGE_FINISH

; ------------------------------------------------
; アンインストーラーページ
; ------------------------------------------------
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_COMPONENTS
!insertmacro MUI_UNPAGE_INSTFILES

; ------------------------------------------------
; 多言語対応
; ------------------------------------------------
!insertmacro MUI_LANGUAGE "Japanese"
!insertmacro MUI_LANGUAGE "English"

; 日本語の文字列
LangString LaunchApp ${LANG_JAPANESE} "${APP_NAME} を起動"
LangString AlreadyRunning ${LANG_JAPANESE} "${APP_NAME} が既に実行中です。先に終了してください。"
LangString NotEnoughSpace ${LANG_JAPANESE} "ディスク容量が不足しています。最低 100 MB の空き容量が必要です。"
LangString RemoveUserData ${LANG_JAPANESE} "設定とユーザーデータを完全に削除する"
LangString RemoveUserDataDesc ${LANG_JAPANESE} "チェックを入れると、以下のフォルダが削除されます：$\r$\n$APPDATA\ProMultiTabNotepad"
LangString KeepUserData ${LANG_JAPANESE} "設定とユーザーデータは保持されました。"
LangString UpdateDetected ${LANG_JAPANESE} "既存のバージョン $0 が検出されました。$\r$\n上書きインストールしますか？"

; 英語の文字列
LangString LaunchApp ${LANG_ENGLISH} "Launch ${APP_NAME}"
LangString AlreadyRunning ${LANG_ENGLISH} "${APP_NAME} is already running. Please close it first."
LangString NotEnoughSpace ${LANG_ENGLISH} "Not enough disk space. At least 100 MB of free space is required."
LangString RemoveUserData ${LANG_ENGLISH} "Remove settings and user data completely"
LangString RemoveUserDataDesc ${LANG_ENGLISH} "If checked, the following folder will be deleted:$\r$\n$APPDATA\ProMultiTabNotepad"
LangString KeepUserData ${LANG_ENGLISH} "Settings and user data have been preserved."
LangString UpdateDetected ${LANG_ENGLISH} "Existing version $0 detected.$\r$\nDo you want to overwrite?"

; ------------------------------------------------
; インストーラーの初期化
; ------------------------------------------------
Function .onInit
  ; 既に実行中かチェック
  System::Call 'kernel32::CreateMutex(i 0, i 0, t "ProMultiTabNotepad_Installer") i .r1 ?e'
  Pop $0
  ${If} $0 != 0
    MessageBox MB_OK|MB_ICONEXCLAMATION "$(AlreadyRunning)"
    Abort
  ${EndIf}

  ; ディスク容量チェック（100 MB）
  ${GetRoot} "$INSTDIR" $0
  ${DriveSpace} "$0\" "/D=F /S=M" $1
  ${If} $1 < 100
    MessageBox MB_OK|MB_ICONSTOP "$(NotEnoughSpace)"
    Abort
  ${EndIf}

  ; 既存バージョンのチェック
  ReadRegStr $0 HKLM "${APP_UNINST_KEY}" "DisplayVersion"
  ${If} $0 != ""
    MessageBox MB_OKCANCEL|MB_ICONQUESTION "$(UpdateDetected)" IDOK continue
    Abort
  continue:
  ${EndIf}
FunctionEnd

; ------------------------------------------------
; インストールセクション
; ------------------------------------------------
Section "MainSection" SEC01
  SetOutPath "$INSTDIR"
  SetOverwrite on

  ; 実行ファイルのコピー
  File "dist\${APP_EXE}"

  ; レジストリにインストール情報を書き込み
  WriteRegStr HKLM "${APP_REG_KEY}" "InstallDir" "$INSTDIR"
  WriteRegStr HKLM "${APP_REG_KEY}" "Version" "${APP_VERSION}"

  ; アンインストーラーの作成
  WriteUninstaller "$INSTDIR\Uninstall.exe"

  ; アンインストール情報の登録
  WriteRegStr HKLM "${APP_UNINST_KEY}" "DisplayName" "${APP_NAME}"
  WriteRegStr HKLM "${APP_UNINST_KEY}" "DisplayVersion" "${APP_VERSION}"
  WriteRegStr HKLM "${APP_UNINST_KEY}" "Publisher" "${APP_PUBLISHER}"
  WriteRegStr HKLM "${APP_UNINST_KEY}" "URLInfoAbout" "${APP_URL}"
  WriteRegStr HKLM "${APP_UNINST_KEY}" "UninstallString" "$INSTDIR\Uninstall.exe"
  WriteRegStr HKLM "${APP_UNINST_KEY}" "DisplayIcon" "$INSTDIR\${APP_EXE}"
  WriteRegDWORD HKLM "${APP_UNINST_KEY}" "NoModify" 1
  WriteRegDWORD HKLM "${APP_UNINST_KEY}" "NoRepair" 1

  ; ファイル関連付けの登録
  Call RegisterFileAssociations

  ; スタートメニューショートカットの作成
  CreateDirectory "$SMPROGRAMS\${APP_NAME}"
  CreateShortcut "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk" "$INSTDIR\${APP_EXE}"
  CreateShortcut "$SMPROGRAMS\${APP_NAME}\Uninstall.lnk" "$INSTDIR\Uninstall.exe"

  ; デスクトップショートカットの作成
  CreateShortcut "$DESKTOP\${APP_NAME}.lnk" "$INSTDIR\${APP_EXE}"

SectionEnd

; ------------------------------------------------
; ファイル関連付け関数
; ------------------------------------------------
Function RegisterFileAssociations
  ; .txt ファイルの関連付け
  WriteRegStr HKCR ".txt\OpenWithProgids" "ProMultiTabNotepad" ""
  
  ; .md ファイルの関連付け
  WriteRegStr HKCR ".md\OpenWithProgids" "ProMultiTabNotepad" ""
  
  ; .html ファイルの関連付け
  WriteRegStr HKCR ".html\OpenWithProgids" "ProMultiTabNotepad" ""
  
  ; .css ファイルの関連付け
  WriteRegStr HKCR ".css\OpenWithProgids" "ProMultiTabNotepad" ""
  
  ; .py ファイルの関連付け
  WriteRegStr HKCR ".py\OpenWithProgids" "ProMultiTabNotepad" ""

  ; ProMultiTabNotepad プログラムIDの登録
  WriteRegStr HKCR "ProMultiTabNotepad" "" "Pro Multi-Tab Notepad Document"
  WriteRegStr HKCR "ProMultiTabNotepad\DefaultIcon" "" "$INSTDIR\${APP_EXE},0"
  WriteRegStr HKCR "ProMultiTabNotepad\shell\open\command" "" '"$INSTDIR\${APP_EXE}" "%1"'

  ; システムにファイル関連付けの変更を通知
  System::Call 'shell32.dll::SHChangeNotify(i, i, i, i) v (0x08000000, 0, 0, 0)'
FunctionEnd

; ------------------------------------------------
; アンインストーラーセクション
; ------------------------------------------------
Section "Uninstall"
  ; 実行中のプロセスを確認（簡易チェック）
  ; FindProcDLL::FindProc を使用しない簡易的な方法
  
  ; ファイルの削除
  Delete "$INSTDIR\${APP_EXE}"
  Delete "$INSTDIR\Uninstall.exe"

  ; ショートカットの削除
  Delete "$DESKTOP\${APP_NAME}.lnk"
  Delete "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk"
  Delete "$SMPROGRAMS\${APP_NAME}\Uninstall.lnk"
  RMDir "$SMPROGRAMS\${APP_NAME}"

  ; インストールディレクトリの削除
  RMDir "$INSTDIR"

  ; レジストリの削除
  DeleteRegKey HKLM "${APP_UNINST_KEY}"
  DeleteRegKey HKLM "${APP_REG_KEY}"

  ; ファイル関連付けの削除
  Call un.UnregisterFileAssociations

SectionEnd

; ------------------------------------------------
; アンインストーラー: ユーザーデータ削除オプション
; ------------------------------------------------
Section /o "un.Remove User Data" SEC_USERDATA
  RMDir /r "$APPDATA\ProMultiTabNotepad"
SectionEnd

; ------------------------------------------------
; アンインストーラー: セクション説明
; ------------------------------------------------
!insertmacro MUI_UNFUNCTION_DESCRIPTION_BEGIN
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC_USERDATA} "$(RemoveUserDataDesc)"
!insertmacro MUI_UNFUNCTION_DESCRIPTION_END

; ------------------------------------------------
; ファイル関連付け解除関数
; ------------------------------------------------
Function un.UnregisterFileAssociations
  ; OpenWithProgids からの削除
  DeleteRegValue HKCR ".txt\OpenWithProgids" "ProMultiTabNotepad"
  DeleteRegValue HKCR ".md\OpenWithProgids" "ProMultiTabNotepad"
  DeleteRegValue HKCR ".html\OpenWithProgids" "ProMultiTabNotepad"
  DeleteRegValue HKCR ".css\OpenWithProgids" "ProMultiTabNotepad"
  DeleteRegValue HKCR ".py\OpenWithProgids" "ProMultiTabNotepad"

  ; ProMultiTabNotepad プログラムIDの削除
  DeleteRegKey HKCR "ProMultiTabNotepad"

  ; システムに変更を通知
  System::Call 'shell32.dll::SHChangeNotify(i, i, i, i) v (0x08000000, 0, 0, 0)'
FunctionEnd
